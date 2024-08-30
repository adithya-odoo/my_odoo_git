# -*- coding: utf-8 -*-

from odoo import api, models


class PurchaseOrder(models.Model):
    """ To add 'Tolerance' field in purchase order line """
    _inherit = 'purchase.order'

    @api.onchange('partner_id', 'product_id')
    def onchange_partner_id(self):
        for line in self:
            line.order_line.update({
                'tolerance' : line.partner_id.tolerance
            })