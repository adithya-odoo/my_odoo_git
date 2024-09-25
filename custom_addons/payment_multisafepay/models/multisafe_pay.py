# -*- coding: utf-8 -*-

from odoo import _, fields, models

from odoo.exceptions import ValidationError


class PaymentProvider(models.Model):
    _inherit = 'payment.provider'

    code = fields.Selection(selection_add=[('multisafepay', 'Multisafepay')],
                            ondelete={'multisafepay': 'set default'})
    multisafepay_api_key = fields.Char(
        string="Multisafepay api key",
        help="The Test or Live API Key depending on the configuration of the provider",
        required_if_provider="multisafepay")