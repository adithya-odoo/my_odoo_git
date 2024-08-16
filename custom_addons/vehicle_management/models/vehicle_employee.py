from odoo import api, fields, models


class VehicleEmployee(models.Model):
    _name = "vehicle.employee"
    _description = "Vehicle Employee"

    managing_id = fields.Many2one('vehicle.management', 'Managing id')
    labor_id = fields.Many2one('hr.employee', "Labour", store=True)
    company_id = fields.Many2one('res.company', store=True, copy=False, string="Company")
    currency_id = fields.Many2one('res.currency', string="Currency",
                                  related='company_id.currency_id',
                                  default=lambda self: self.env.user.company_id.currency_id.id)
    hourly_cost = fields.Monetary('Hourly Cost', related="labor_id.hourly_cost", currency_field='currency_id',
                                  default=0.0)
    time_spent = fields.Integer(string="Time Spent", default=1)
    sub_total_time_cost = fields.Monetary(string="Sub total cost", default=0.0)

    @api.onchange('time_spent', 'hourly_cost')
    def _total_time_cost_calculate(self):
        if self.time_spent:
            self.sub_total_time_cost = self.time_spent * self.hourly_cost
