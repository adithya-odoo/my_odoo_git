# -*- coding: utf-8 -*-
import logging
import requests
import pprint


from odoo import _, fields, models

from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class PaymentProvider(models.Model):
    _inherit = 'payment.provider'

    code = fields.Selection(selection_add=[('multisafepay', 'Multisafepay')],
                            ondelete={'multisafepay': 'set default'})
    multisafepay_api_key = fields.Char(
        string="Multisafepay api key",
        help="The Test or Live API Key depending on the configuration of the provider",
        required_if_provider="multisafepay")

    def _multisafepay_make_request(self, data=None, method='POST'):
        print("ftt")
        if method == 'POST':
            self.ensure_one()
            url = f'https://testapi.multisafepay.com/v1/json/orders?api_key={self.multisafepay_api_key}'

            headers = {
                 "Accept": "application/json",
                "Content-Type": "application/json",
            }

            response = requests.request(method, url, json=data, headers=headers)
            try:
                response.raise_for_status()
            except requests.exceptions.HTTPError:
                _logger.exception(
                    "Invalid API request at %s with data:\n%s", url,
                    pprint.pformat(data))
                raise ValidationError(
                    "Multisafepay: " + _(
                        "The communication with the API failed. Mollie gave us the following "
                        "information: %s", response.json().get('detail', '')))
            except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
                   _logger.exception("Unable to reach endpoint at %s", url)
                   raise ValidationError(
                   "Multisafepay: " + _("Could not establish the connection to the API."))

            print(response.text)
            return response.json()

        elif method == 'GET':
            url = f'https://testapi.multisafepay.com/v1/json/orders/{data}?api_key={self.multisafepay_api_key}'
            headers = {"accept": "application/json"}
            response = requests.request(method, url, headers=headers)
            print(response.text)
            return response.json()
