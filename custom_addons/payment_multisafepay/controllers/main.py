# -*- coding: utf-8 -*-

import logging
import pprint

from odoo import http
from odoo.exceptions import ValidationError
from odoo.http import request

# _logger = logging.getLogger(__name__)


class MultisafepayController(http.Controller):
    _return_url = '/payment/Multisafepay/return'
    # _webhook_url = '/payment/mollie/webhook'

    @http.route(_return_url, type='http', auth='public', methods=['GET', 'POST'], csrf=False,
        save_session=False)
    def Multisafepay_return_from_checkout(self, **data):
        request.env['payment.transaction'].sudo()._handle_notification_data('multisafepay', data)
        return request.redirect('/payment/status')
