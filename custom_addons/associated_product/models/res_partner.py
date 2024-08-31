# -*- coding: utf-8 -*-

from odoo import fields, models


class ResPartner(models.Model):
    """ To add 'associated_product_ids' many2many field in 'res.partner' model """
    _inherit = 'res.partner'

    associated_product_ids = fields.Many2many(comodel_name='product.template',
                                              relation='product_partner_rel',
                                              string="Associated product")

