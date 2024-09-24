# -*- coding: utf-8 -*-
from email.policy import default

from odoo import fields, models


class DiscountSession(models.Model):
    """ To insert a Discount limit field inside the pos settings"""
    _inherit = 'pos.config'

    company_id = fields.Many2one(comodel_name='res.company', store=True,
                                 copy=False, string="Company")
    currency_id = fields.Many2one('res.currency', string="Currency",
                                  related='company_id.currency_id',
                                  default=lambda
                                      self: self.env.user.company_id.currency_id.id)
    is_discount = fields.Boolean(string="Discount", default=False)
    type = fields.Selection(selection=[
            ('amount', "Amount"),
            ('percentage', "Percentage"),
        ], string="Discount Type")
    discount_limit = fields.Monetary(string="Discount Limit")
    discount_limit_percentage = fields.Float(string="Discount Percentage")