# -*- coding: utf-8 -*-

from odoo import api,fields, models


class SaleOrder(models.Model):
    """ To set a new field inside the 'sale.order.line' """
    _inherit = 'sale.order'

    @api.onchange('order_line', 'partner_id')
    def onchange_partner(self):
        for rec in self:
            rec.order_line.tolerance = rec.partner_id.tolerance

    @api.onchange('purchase_order_count')
    def check_purchase_order(self):
        print("hello")
        if self.purchase_order_count != 0:
            print("hello")