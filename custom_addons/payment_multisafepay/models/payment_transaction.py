# -*- coding: utf-8 -*-

import logging
import pprint
from werkzeug import urls

from odoo import _, models
from odoo.exceptions import ValidationError

from odoo.addons.payment import utils as payment_utils

from odoo.addons.payment_multisafepay.controllers.main import MultisafepayController

_logger = logging.getLogger(__name__)


class PaymentTransaction(models.Model):
    """ To sent transaction details and api key to the payment provider"""
    _inherit = 'payment.transaction'

    def _get_specific_rendering_values(self, processing_values):
        """To render to the function"""
        res = super()._get_specific_rendering_values(processing_values)
        if self.provider_code != 'multisafepay':
            return res

        payload = self._multisafepay_prepare_payment_request_payload()
        _logger.info("sending '/payments' request for link creation:\n%s",
                     pprint.pformat(payload))
        payment_data = self.provider_id._multisafepay_make_request(data=payload)

        # The provider reference is set now to allow fetching the payment status after redirection
        self.provider_reference = payment_data.get('id')

        # Extract the checkout URL from the payment data and add it with its query parameters to the
        # rendering values. Passing the query parameters separately is necessary to prevent them
        # from being stripped off when redirecting the user to the checkout URL, which can happen
        # when only one payment method is enabled on Mollie and query parameters are provided.
        checkout_url = payment_data['data']['payment_url']
        parsed_url = urls.url_parse(checkout_url)
        url_params = urls.url_decode(parsed_url.query)
        return {'api_url': checkout_url, 'url_params': url_params}

    def _multisafepay_prepare_payment_request_payload(self):
        """to set payload to transfer to main function"""
        base_url = self.provider_id.get_base_url()
        redirect_url = urls.url_join(base_url, MultisafepayController._return_url)
        cancel_url = urls.url_join(base_url, MultisafepayController._cancel_url)
        cancel_url_params = {
            'tx_ref': self.reference,
            'return_access_tkn': payment_utils.generate_access_token(self.reference),
        }

        return {
           "type": "redirect",
            "order_id": self.reference,
            "gateway": "",
            "currency":  self.currency_id.name,
            "amount":  self.amount * 100,
              "description": "order disc",
             "payment_options": {
               "notification_method": "POST",
              "redirect_url": f'{redirect_url}?ref={self.reference}',
              "close_window": True
             },
             "customer": {
             "locale": self.partner_lang,
             "ip_address": "123.123.123.123",
              "first_name": "Mitchell",
              "last_name": "Admin",
              "company_name": self.company_id.name,
                "address1": self.partner_city,
                  "house_number": "211",
               "zip_code": self.partner_zip,
                "city": self.partner_city,
                "country": self.partner_country_id.name,
                "phone": self.partner_phone,
                 "email": self.partner_email,
             }
        }

    def _get_tx_from_notification_data(self, provider_code, notification_data):
        """ Override of payment to find the transaction based on Multisafepay data.

        :param str provider_code: The code of the provider that handled the transaction
        :param dict notification_data: The notification data sent by the provider
        :return: The transaction if found
        :rtype: recordset of `payment.transaction`
        :raise: ValidationError if the data match no transaction
        """
        tx = super()._get_tx_from_notification_data(provider_code, notification_data)
        if provider_code != 'multisafepay' or len(tx) == 1:
            return tx

        tx = self.search(
            [('reference', '=', notification_data.get('ref')), ('provider_code', '=', 'multisafepay')])
        if not tx:
            raise ValidationError("Multisafepay: " + _(
                "No transaction found matching reference %s.",
                notification_data.get('ref')))
        return tx

    def _process_notification_data(self, notification_data):
        """ Override of payment to process the transaction based on Mollie data.

        Note: self.ensure_one()

        :param dict notification_data: The notification data sent by the provider
        :return: None
        """
        super()._process_notification_data(notification_data)
        if self.provider_code != 'multisafepay':
            return
        transaction_id = notification_data['transactionid']
        payment_data = self.provider_id._multisafepay_make_request(data=transaction_id, method="GET")

        # Update the payment method.
        payment_method_type = payment_data.get('method', '')
        if payment_method_type == 'creditcard':
            payment_method_type = payment_data.get('details', {}).get('cardLabel', '').lower()
        payment_method = self.env['payment.method']._get_from_code(payment_method_type)
        self.payment_method_id = payment_method or self.payment_method_id

        # Update the payment state.
        payment_status = payment_data['data']['status']
        if payment_status in ['initialized', 'uncleared']:
            self._set_pending()
        elif payment_status in ['completed', 'shipped']:
            self._set_done()
        elif payment_status in ['void', 'declined', ]:
            self._set_canceled("Multisafepay: " + _("Canceled payment with status: %s", payment_status))
        else:
            _logger.info(
                "received data with invalid payment status (%s) for transaction with reference %s",
                payment_status, self.reference
            )
            self._set_error(
                "Multisafepay: " + _("Received data with invalid payment status: %s", payment_status))