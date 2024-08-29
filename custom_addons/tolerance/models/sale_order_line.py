# -*- coding: utf-8 -*-

from odoo import api,fields, models


class SaleOrderLine(models.Model):
    """ To set a new field inside the 'sale.order.line' """
    _inherit = 'sale.order.line'

    tolerance = fields.Float(string="Tolerance")
