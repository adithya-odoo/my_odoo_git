# -*- coding: utf-8 -*-

from odoo import api, fields, models


class PosOrderLine(models.Model):
    """To add a field to show discount amount of order line"""
    _inherit = 'pos.order.line'

    discount_amount = fields.Float(string="Discount Amount", compute="_compute_discount_amount")

    @api.depends('qty', 'price_unit', 'discount')
    def _compute_discount_amount(self):
        """To compute discount amount of each order line"""
        for rec in self:
            if rec.tax_ids_after_fiscal_position.amount:
                rec.discount_amount = (rec.qty * rec.price_unit * (
                            (rec.tax_ids_after_fiscal_position.amount + 100) / 100)) * (
                                              rec.discount / 100)
            else:
                rec.discount_amount = rec.qty * rec.price_unit * (rec.discount / 100)



