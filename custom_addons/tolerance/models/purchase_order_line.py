# -*- coding: utf-8 -*-

from odoo import api, fields, models


class PurchaseOrder(models.Model):
    """ To add 'Tolerance' field in purchase order line """
    _inherit = 'purchase.order'

    @api.onchange('partner_id')
    def onchange_partner_id(self):
        for line in self:
            line.order_line.update({
                'tolerance' : self.partner_id.tolerance
            })

class PurchaseOrderLine(models.Model):
    """ To add 'Tolerance' field in purchase order line """
    _inherit = 'purchase.order.line'

    tolerance = fields.Float(string="Tolerance")
