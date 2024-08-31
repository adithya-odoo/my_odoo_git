# -*- coding: utf-8 -*-

from odoo import api, fields, models


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    @api.onchange('partner_id')
    def onchange_partner_order_line(self):
        """ To insert value inside the tolerance field in sale order"""
        for rec in self.order_line:
            rec.update({
                'tolerance': rec.partner_id.tolerance
            })

class PurchaseOrderLine(models.Model):
    """ To add 'Tolerance' field in purchase order line """
    _inherit = 'purchase.order.line'

    tolerance = fields.Float(string="Tolerance")

    # @api.onchange('product_id')
    # def onchange_partner_order_line(self):
    #     """ To insert value inside the tolerance field in sale order"""
    #     for rec in self:
    #         rec.update({
    #             'tolerance': rec.partner_id.tolerance
    #         })