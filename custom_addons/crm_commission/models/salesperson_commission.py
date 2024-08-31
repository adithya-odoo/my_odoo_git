# -*- coding: utf-8 -*-

from odoo import fields, models

class SalespersonCommission(models.Model):
    """ To insert crm commission (one2many) field inside salesperson """
    _name = 'salesperson.commission'

    users_commission_id = fields.Many2one(comodel_name='res.users',
                                         string='Commission')
    company_id = fields.Many2one(comodel_name='res.company', store=True,
                                 copy=False, string="Company",
                                 default=lambda self: self.env.company)
    currency_id = fields.Many2one(comodel_name='res.currency',
                                  string="Currency",
                                  related='company_id.currency_id',
                                  default=lambda
                                      self: self.env.user.company_id.currency_id.id)
    commission_name = fields.Char(string="Commission Name")
    sale_amount = fields.Monetary(string="Sale Amount")
    rate = fields.Monetary(string="Rate")
    commission = fields.Float(string="Commission")
