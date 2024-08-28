# -*- coding: utf-8 -*-

from odoo import fields, models

class ResUsers(models.Model):
    """ To insert crm commission field inside salesperson """
    _inherit = 'res.users'

    crm_commission_id = fields.Many2one(comodel_name='crm.commission',
                                        string="Commission")
    users_commission_ids = fields.One2many(comodel_name='salesperson.commission',
                                          inverse_name='users_commission_id',
                                          string="Salesperson commission")