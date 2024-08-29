# -*- coding: utf-8 -*-

from odoo import api, fields, models

from odoo.exceptions import ValidationError


class CommissionGraduated(models.Model):
    """ for product if product wise is selected"""
    _name = "commission.graduated"
    _description = "Commission Graduated"

    managing_id = fields.Many2one(comodel_name='crm.commission',
                                 string= "managing_id")
    company_id = fields.Many2one(comodel_name='res.company', store=True,
                                 copy=False, string="Company",
                                 default=lambda self: self.env.company)
    currency_id = fields.Many2one(comodel_name='res.currency',
                                  string="Currency",
                                  related='company_id.currency_id',
                                  default=lambda
                                      self: self.env.user.company_id.currency_id.id)
    from_amount = fields.Monetary(string="From Amount")
    to_amount = fields.Monetary(string="To Amount")
    commission = fields.Float(string="Employee Commission")
    rate = fields.Monetary(string="Rate", compute='compute_calculate_rate',
                           store=True)

    @api.depends('from_amount', 'to_amount', 'commission')
    def compute_calculate_rate(self):
        """To calculate the total rate"""
        for rec in self:
            total_amount = rec.from_amount + rec.to_amount
            rec.rate = total_amount * rec.commission

    @api.constrains('from_amount', 'to_amount')
    def onchange_from_to_amount(self):
        """ To check the To amount is larger than From amount """
        for rec in self:
            if rec.to_amount < rec.from_amount:
                raise ValidationError(
                             'To amount should not be smaller than from amount')
