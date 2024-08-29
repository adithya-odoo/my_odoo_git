# -*- coding: utf-8 -*-

from odoo import fields, models


class ResPartner(models.Model):
    """ To add 'Tolerance' field in 'res.partner' model """
    _inherit = 'res.partner'

    tolerance = fields.Float(string="Tolerance")