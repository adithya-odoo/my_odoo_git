# -*- coding: utf-8 -*-

from odoo import api, fields, models


class VehicleEmployee(models.Model):
    _name = "vehicle.employee"
    _description = "Vehicle Employee"

    managing_id = fields.Many2one(comodel_name='vehicle.management',
                                  string='Managing id')
    labor_id = fields.Many2one(comodel_name='hr.employee', string="Labour",
                               store=True)
    product_id = fields.Many2one(comodel_name='product.product',
                                 string="Product",
                                 domain="[('detailed_type', 'in', ['service'])]",
                                 store=True)
    company_id = fields.Many2one(comodel_name='res.company', store=True,
                                 copy=False, string="Company")
    currency_id = fields.Many2one('res.currency', string="Currency",
                                  related='company_id.currency_id',
                                  default=lambda self: self.env.user.company_id.currency_id.id)
    hourly_cost = fields.Monetary('Hourly Cost',
                                  related="labor_id.hourly_cost",
                                  currency_field='currency_id', default=0.0)
    time_spent = fields.Integer(string="Time Spent", default=1)
    sub_total_time_cost = fields.Monetary(string="Sub total cost", default=0.0)

    @api.onchange('time_spent', 'hourly_cost')
    def _sub_total_time_cost_calculate(self):
        """ To calculate the subtotal of labor cost
            sub_total_time_cost = time_spent * hourly_cost """
        if self.time_spent:
            self.sub_total_time_cost = self.time_spent * self.hourly_cost
