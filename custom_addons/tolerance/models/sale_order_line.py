# -*- coding: utf-8 -*-

from odoo import api, fields, models


class SaleOrderLine(models.Model):
    """ To set a new field inside the 'sale.order.line' """
    _inherit = 'sale.order.line'

    tolerance = fields.Float(string="Tolerance")

    @api.onchange('product_template_id')
    def onchange_partner_order_line(self):
        """ To insert value inside the tolerance field in sale order"""
        print(self.order_partner_id)
        for rec in self:
            rec.write({
                'tolerance': rec.order_partner_id.tolerance
            })
