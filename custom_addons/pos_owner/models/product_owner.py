# -*- coding: utf-8 -*-

from odoo import fields, models

class ProductOwner(models.Model):
    """ To insert new field inside the product form"""
    _inherit = 'product.template'

    product_owner_id = fields.Many2one(comodel_name='res.partner', string='Owner')


