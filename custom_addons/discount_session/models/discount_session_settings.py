# -*- coding: utf-8 -*-
from email.policy import default

from odoo import fields, models


class DiscountConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    pos_is_discount = fields.Boolean(related='pos_config_id.is_discount',
                                     string="Discount", readonly=False)
    pos_type = fields.Selection(selection=[
        ('amount', "Amount"),
        ('Percentage', "Percentage")],
        string="Discount Type", related="pos_config_id.type", readonly=False)
    pos_discount_limit = fields.Monetary(related='pos_config_id.discount_limit',
                                         readonly=False, string='Discount Limit (PoS)')
    pos_discount_limit_percentage = fields.Float(related='pos_config_id.discount_limit_percentage',
                                             string="Discount Percentage", readonly=False)