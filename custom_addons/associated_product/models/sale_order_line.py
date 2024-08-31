# -*- coding: utf-8 -*-

from odoo import fields, models

class SaleOrderLine(models.Model):
    """ To set a new field inside the 'sale.order.line' """
    _inherit = 'sale.order.line'

    is_line_associated_product = fields.Boolean(readonly=True, default=False)