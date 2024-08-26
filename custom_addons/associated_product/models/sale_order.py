# -*- coding: utf-8 -*-

from odoo import api, Command,fields, models


class SalesOrder(models.Model):
    _inherit = 'sale.order'

    is_associated_product = fields.Boolean(string="Associated product", default=False)

    @api.onchange('is_associated_product', 'partner_id')
    def _onchange_associated_product(self):
        """ If the associated product is true it will add the associated product inside the customer form to order line """
        if self.is_associated_product and self.partner_id:
            for record in self.partner_id.associated_product_ids:
                self.order_line = [Command.create({'product_template_id': record.id,
                                                       'name': record.default_code,
                                                       'product_uom_qty': 1,
                                                       'is_line_associated_product': True,
                                                       'price_unit': record.list_price,
                                                        })]

        else:
            for rec in self.order_line:
                if rec.is_line_associated_product:
                    self.write({
                      'order_line': [Command.unlink(rec.id)]
                 })
