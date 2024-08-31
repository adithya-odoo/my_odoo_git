# -*- coding: utf-8 -*-

from odoo import api, fields, models


class SalesOrder(models.Model):
    _inherit = 'sale.order'

    associated_product = fields.Boolean(string="Associated product", default=False)
    @api.onchange('associated_product', 'partner_id')
    def _compute_associated_product(self):
        """ If the associated product is true it will add the associated product inside the customer form to order line """
        if self.associated_product == True:
            print(self.partner_id.associated_product_ids)
        # for record in self.partner_id.associated_product_ids:










