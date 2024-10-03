# -*- coding: utf-8 -*-

from odoo import http
from odoo.http import request


class MultisafepayController(http.Controller):
    _return_url = '/payment/Multisafepay/return'


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