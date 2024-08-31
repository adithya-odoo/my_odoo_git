# -*- coding: utf-8 -*-

from odoo import api, fields, models


class PurchaseOrderLine(models.Model):
    """ To add 'Tolerance' field in purchase order line """
    _inherit = 'purchase.order.line'

    tolerance = fields.Float(string="Tolerance", compute='compute_tolerance',
                             readonly=False, store=True)

    @api.depends('partner_id')
    def compute_tolerance(self):
        """ To compute the value in tolerance"""
        for rec in self:
            rec.update({
                'tolerance': rec.partner_id.tolerance
            })