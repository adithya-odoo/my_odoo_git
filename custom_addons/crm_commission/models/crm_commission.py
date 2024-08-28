# -*- coding: utf-8 -*-

from odoo import api, fields, models, _

from odoo.exceptions import ValidationError


class CrmCommission(models.Model):
    """ To setup crm commission plan"""
    _name = 'crm.commission'
    _description = 'Crm Commission'

    name = fields.Char(string="Name", required=True)
    is_active = fields.Boolean(string="Active", default=True)
    from_date = fields.Date(string="From Date")
    to_date = fields.Date(string="To Date")
    type = fields.Selection(selection=[('product wise', 'Product Wise'),
                                       ('revenue wise', 'Revenue Wise')],
                            string="Type",
                            default='product wise')
    product_ids = fields.One2many(comodel_name='commission.product',
                                  inverse_name='management_id')
    revenue_wise = fields.Selection(selection=[('straight', 'Straight'),
                                               ('graduated', 'Graduated')],
                                    default="straight", string="Revenue Type")
    company_id = fields.Many2one(comodel_name='res.company', store=True,
                                 copy=False, string="Company",
                                 default=lambda self: self.env.company)
    currency_id = fields.Many2one(comodel_name='res.currency', string="Currency",
                                  related='company_id.currency_id',
                                  default=lambda
                                self: self.env.user.company_id.currency_id.id)
    sequence = fields.Char(string='Sequence', default=lambda self: _('New'),
                           copy=False, readonly=True, tracking=True)
    from_amount = fields.Monetary(string="From Amount")
    to_amount = fields.Monetary(string="To Amount")
    commission = fields.Float(string="Employee Commission")
    rate = fields.Monetary(string="Rate", compute='compute_calculate_rate')
    graduated_ids = fields.One2many(comodel_name='commission.graduated',
                                    inverse_name='managing_id')

    @api.model_create_multi
    def create(self, vals_list):
        """ To create vehicle service form sequence """
        for vals in vals_list:
            if vals.get('sequence', _('New')) == _('New'):
                vals['sequence'] = (self.env['ir.sequence'].next_by_code('commission.sequence'))
        return super().create(vals_list)

    @api.depends('from_amount', 'to_amount', 'commission')
    def compute_calculate_rate(self):
        """To calculate the total rate"""
        total_amount = self.from_amount + self.to_amount
        self.rate = total_amount * self.commission

    @api.constrains('from_amount', 'to_amount')
    def onchange_from_to_amount(self):
        if self.to_amount < self.from_amount:
            raise ValidationError('To amount should not be smaller than from amount')

