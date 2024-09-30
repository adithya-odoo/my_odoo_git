# -*- coding: utf-8 -*-

from odoo import http

from odoo.http import request

from odoo.addons.payment import utils as payment_utils

from werkzeug.exceptions import Forbidden


class MultisafepayController(http.Controller):
    _return_url = '/payment/Multisafepay/return'
    _cancel_url = '/payment/Multisafepay/cancel/'


    @http.route(_return_url, type='http', auth='public', methods=['GET', 'POST'], csrf=False,
        save_session=False)

    def Multisafepay_return_from_checkout(self, **data):
        """ Process the PDT notification sent by Multisafepay after redirection from checkout.

               The PDT (Payment Data Transfer) notification contains the parameters necessary to verify the
               origin of the notification and retrieve the actual notification data, if PDT is enabled on
               the account.

               The route is flagged with `save_session=False` to prevent Odoo from assigning a new session
               to the user if they are redirected to this route with a POST request. Indeed, as the session
               cookie is created without a `SameSite` attribute, some browsers that don't implement the
               recommended default `SameSite=Lax` behavior will not include the cookie in the redirection
               request from the payment provider to Odoo. As the redirection to the '/payment/status' page
               will satisfy any specification of the `SameSite` attribute, the session of the user will be
               retrieved and with it the transaction which will be immediately post-processed.

               :param dict pdt_data: The PDT notification data send by Multisafepay.
               """
        request.env['payment.transaction'].sudo()._handle_notification_data('multisafepay', data)
        return request.redirect('/payment/status')

    # @http.route(_cancel_url, type='http', auth='public', methods=['GET'],csrf=False, save_session=False)
    # def multisafepay_return_from_canceled_checkout(self, tx_ref, return_access_tkn):
    #     """ Process the transaction after the customer has canceled the payment.
    #
    #     :param str tx_ref: The reference of the transaction having been canceled.
    #     :param str return_access_tkn: The access token to verify the authenticity of the request.
    #                                   multisafepay forbids any parameter with the name "token" inside.
    #     """
    #
    #     tx_sudo = request.env['payment.transaction'].sudo()._get_tx_from_notification_data(
    #         'multisafepay', {'item_number': tx_ref}
    #     )
    #     if not payment_utils.check_access_token(return_access_tkn, tx_ref):
    #         raise Forbidden()
    #     tx_sudo._handle_notification_data('paypal', {})
    #
    #     return request.redirect('/payment/status')
