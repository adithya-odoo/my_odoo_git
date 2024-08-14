from datetime import timedelta

from odoo import api, fields, models


class VehicleManagement(models.Model):
    _name = "vehicle.management"
    _description = "Vehicle Management"
    _inherit = ['mail.thread']

    name = fields.Char(string="Name")
    address = fields.Text(string="Address")
    advisor_id = fields.Many2one('res.users', "Service advisor")
    model_id = fields.Many2one('fleet.vehicle.models', " Vehicle Model")
    vehicle_type = fields.Selection(related='model_id.vehicle_type', string="Vehicle type", readonly=False)
    active = fields.Boolean(string="Active")
    state = fields.Selection(selection=[('draft', 'Draft'), ('done', 'Done'), ('in_progress', 'In_progress'), ('done',
                                        'Done'), ('cancelled', 'Cancelled')], default='draft', required=True
                             , tracking=True)
    phone = fields.Char(string="Phone")
    vehicle_number = fields.Integer(string="Vehicle number", copy=False)
    image = fields.Image(string="Image")
    start_date = fields.Date('Start Date', readonly='true', required=True, default=fields.Date.today())
    duration_time = fields.Integer(string="Duration")
    delivery_date = fields.Date(string="Delivery date")
    service_type = fields.Selection([('paid', 'Paid'), ('free', 'Free')])
    estimated_amount = fields.Integer(string="Estimated amount")
    customer_complaint = fields.Text(string="Complaint")

    @api.onchange('duration_time')
    def calculate_delivery_date(self):
        if self.duration_time:
            self.delivery_date = self.start_date + timedelta(days=self.duration_time)
