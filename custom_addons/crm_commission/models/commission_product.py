# -*- coding: utf-8 -*-

from odoo import api, fields, models


class CommissionProduct(models.Model):
    """ for product if product wise is selected"""
    _name = "commission.product"
    _description = "commission product"

    management_id = fields.Many2one(comodel_name='crm.commission',
                                    string="management_id")
    product_id = fields.Many2one(comodel_name='product.template',
                                 string="Product", store=True)
    product_category = fields.Many2one(string="Category",
                                       related='product_id.categ_id')
    company_id = fields.Many2one(comodel_name='res.company', store=True,
                                 copy=False, string="Company",
                                 default=lambda self: self.env.company)
    currency_id = fields.Many2one(comodel_name='res.currency', string="Currency",
                                  related='company_id.currency_id',
                                  default=lambda self: self.env.user.company_id.currency_id.id)
    rate_percentage = fields.Float("Rate")
    max_commission_amount = fields.Monetary(string="Maximum amount",
                                            compute="compute_max_amount",
                                            store=True)

    @api.depends('rate_percentage', 'product_id')
    def compute_max_amount(self):
        """ To calculate the max_commission_amount
            commission amount = product_price * percentage"""
        self.max_commission_amount = self.product_id.list_price * self.rate_percentage
