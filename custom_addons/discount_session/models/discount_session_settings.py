# -*- coding: utf-8 -*-

from odoo import fields, models


class DiscountConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    pos_discount_limit = fields.Monetary(related='pos_config_id.discount_limit', readonly=False, string='Discount Limit (PoS)')