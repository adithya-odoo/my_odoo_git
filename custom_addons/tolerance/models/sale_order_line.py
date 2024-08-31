# -*- coding: utf-8 -*-

from odoo import api, fields, models


class SaleOrderLine(models.Model):
    """ To set a new field inside the 'sale.order.line' """
    _inherit = 'sale.order.line'

    tolerance = fields.Float(string="Tolerance", compute='compute_tolerance',
                             readonly=False, store=True)

    @api.depends('order_partner_id')
    def compute_tolerance(self):
        """ To compute the value in tolerance"""
        for rec in self:
            rec.update({
                'tolerance': rec.order_partner_id.tolerance
            })