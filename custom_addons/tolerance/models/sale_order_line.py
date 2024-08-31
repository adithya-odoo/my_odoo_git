# -*- coding: utf-8 -*-

from odoo import api, fields, models

class SaleOrder(models.Model):
    """ To set a new field inside the 'sale.order.line' """
    _inherit = 'sale.order'

    @api.onchange('partner_id')
    def onchange_partner_order_line(self):
        """ To insert value inside the tolerance field in sale order"""
        for line in self.order_line:
            line.update({
               'tolerance': line.order_partner_id.tolerance
            })

class SaleOrderLine(models.Model):
    """ To set a new field inside the 'sale.order.line' """
    _inherit = 'sale.order.line'

    tolerance = fields.Float(string="Tolerance", store=True)
