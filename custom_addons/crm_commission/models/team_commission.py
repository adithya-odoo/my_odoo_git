# -*- coding: utf-8 -*-

from odoo import fields, models

class TeamCommission(models.Model):
    """ To insert crm commission (one2many) field inside sales team """
    _name = 'team.commission'

    team_commission_id = fields.Many2one(comodel_name='crm.team',
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



