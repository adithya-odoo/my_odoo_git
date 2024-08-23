# -*- coding: utf-8 -*-
import datetime

from odoo import Command, fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    associated_product_ids = fields.Many2many('product.product', 'product_partner_rel', string="Associated product")

