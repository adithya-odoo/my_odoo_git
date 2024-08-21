# -*- coding: utf-8 -*-

from odoo import api, fields, models


class VehicleProduct(models.Model):
    _name = "vehicle.product"
    _description = "Vehicle product"

    management_id = fields.Many2one('vehicle.management', "management_id")
    product_id = fields.Many2one('product.product', "Product",
                                 domain="[('detailed_type', 'in', ['consu', 'product'])]", store=True)
    company_id = fields.Many2one('res.company', store=True, copy=False, string="Company")
    currency_id = fields.Many2one('res.currency', string="Currency",
                                  related='company_id.currency_id',
                                  default=lambda self: self.env.user.company_id.currency_id.id)
    quantity = fields.Float(string="Quantity", default=1)
    product_price = fields.Float('Price', related="product_id.list_price", currency_field='currency_id',
                                 default=0.0)
    product_sub_total = fields.Monetary(string="Sub total")

    @api.onchange('product_id', 'quantity')
    def _subtotal_product_cost_calculate(self):
        """ To calculate the subtotal of product price
                              product_sub_total = product_price * quantity """
        if self.quantity:
            self.product_sub_total = self.quantity * self.product_price
