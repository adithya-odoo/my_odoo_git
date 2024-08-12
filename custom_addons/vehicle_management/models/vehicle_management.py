# -*- coding: utf-8 -*-

from datetime import timedelta

from odoo import api, fields, models, _


class VehicleManagement(models.Model):
    _name = "vehicle.management"
    _description = "Vehicle Management"
    _inherit = ['mail.thread']

    reference_no = fields.Char('Reference', default=lambda self: _('New'), copy=False, readonly=True, tracking=True)
    partner_id = fields.Many2one('res.partner', string="Name", required=True)
    advisor_id = fields.Many2one('res.users', "Service advisor")
    vehicle_id = fields.Many2one('fleet.vehicle.model', " Vehicle Model", domain="[('category_id', '=', vehicle_type)]")
    vehicle_type = fields.Many2one('fleet.vehicle.model.category', string="Vehicle type",
                                   related='vehicle_id.category_id')
    active = fields.Boolean(default=True)
    state = fields.Selection(selection=[('draft', 'Draft'), ('done', 'Done'), ('progress', 'Progress'), ('done',
                                        'Done'), ('cancelled', 'Cancelled')], default='draft', required=True
                             , tracking=True)
    phone = fields.Char(related='partner_id.phone', string="Phone", readonly=False)
    vehicle_number = fields.Char(string="Vehicle number", copy=False)
    image = fields.Image(string="Image")
    start_date = fields.Date('Start Date', readonly='true', required=True, default=fields.Date.today())
    duration_time = fields.Integer(string="Duration")
    delivery_date = fields.Date(string="Delivery date")
    service_type = fields.Selection([('paid', 'Paid'), ('free', 'Free')])
    estimated_amount = fields.Float(string="Estimated amount")
    customer_complaint = fields.Text(string="Complaint")
    company_name = fields.Many2one('res.company', "Company", default=lambda self: self.env.company)

    @api.onchange('duration_time')
    def calculate_delivery_date(self):
        if self.duration_time:
            self.delivery_date = self.start_date + timedelta(days=self.duration_time)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('reference_no', _('New')) == _('New'):
                vals['reference_no'] = self.env['ir.sequence'].next_by_code('vehicle.reference')
        return super().create(vals_list)

    def confirm_button(self):
        self.write({
            'state': "progress"
        })

    _sql_constraints = [
                     ('field_unique',
                      'unique(vehicle_number)',
                      'Vehicle number is already exits')
                       ]



