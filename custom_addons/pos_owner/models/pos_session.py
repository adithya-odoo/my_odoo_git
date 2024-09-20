# -*- coding: utf-8 -*-

from odoo import models

class PosSession(models.Model):
    """To append the product_owner_id field in pos"""
    _inherit = 'pos.session'

    def _loader_params_product_product(self):
        result = super()._loader_params_product_product()
        result['search_params']['fields'].append('product_owner_id')
        return result