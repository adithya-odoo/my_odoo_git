# -*- coding: utf-8 -*-
import datetime
from datetime import timedelta

from odoo import api, fields, models, _

from odoo.exceptions import ValidationError


class VehicleManagement(models.Model):
    _name = "vehicle.management"
    _description = "Vehicle Management"
    _inherit = ['mail.thread']

    name = fields.Char('Reference', default=lambda self: _('New'), copy=False,
                       readonly=True, tracking=True)
    partner_id = fields.Many2one('res.partner', string="Name", required=True)
    advisor_id = fields.Many2one('res.users', "Service advisor", required=True)
    vehicle_id = fields.Many2one('fleet.vehicle.model', " Vehicle Model",
                                 domain="[('category_id', '=', vehicle_type_id)]",
                                 required=True)
    vehicle_type_id = fields.Many2one('fleet.vehicle.model.category', string="Vehicle type",
                                      related='vehicle_id.category_id', store=True)
    active = fields.Boolean(default=True, related="partner_id.active", readonly=False)
    state = fields.Selection(selection=[('draft', 'Draft'),
                                        ('done', 'Done'),
                                        ('progress', 'Progress'),
                                        ('done', 'Done'),
                                        ('ready for delivery', 'Ready For Delivery'),
                                        ('cancelled', 'Cancelled')],
                             default='draft', required=True, tracking=True)
    phone = fields.Char(related='partner_id.phone', string="Phone", readonly=False)
    vehicle_number = fields.Char(string="Vehicle number", copy=False, required=True)
    image = fields.Image(string="Image")
    start_date = fields.Date('Start Date',
                             required=True,
                             default=fields.Date.today())
    duration_time = fields.Integer(string="Duration")
    delivery_date = fields.Date(string="Delivery date")
    service_type = fields.Selection([('paid', 'Paid'), ('free', 'Free')], default="paid")
    estimated_amount = fields.Float(string="Estimated amount")
    customer_complaint = fields.Text(string="Complaint")
    company_id = fields.Many2one('res.company', store=True, copy=False, string="Company",
                                 default=lambda self: self.env.company)
    currency_id = fields.Many2one('res.currency', string="Currency",
                                  related='company_id.currency_id',
                                  default=lambda self: self.env.user.company_id.currency_id.id)
    tag_ids = fields.Many2many('repair.tag', 'repair_tag_rel', string='Tags',
                               help="Repair tags")
    color = fields.Integer('Color Index', default=0)
    labour_line_ids = fields.One2many('vehicle.employee', 'managing_id')
    product_line_ids = fields.One2many('vehicle.product', 'management_id')
    total_product_cost = fields.Monetary(string="Total cost", readonly=True, default=0.0)
    total_time_cost = fields.Monetary(string="Total cost", readonly=True, default=0.0)
    total_cost = fields.Monetary(string="Total cost", default=0.0)
    smart_partner = fields.Integer(compute='vehicle_history')
    estimated_delivery_date = fields.Date(string="Estimated delivery date")
    invoice_status = fields.Selection([('invoice draft', 'Invoice Draft'), ('invoiced', 'Invoiced')],
                                      default="invoice draft")

    def vehicle_history(self):
        for record in self:
            record.smart_partner = self.env['vehicle.management'].search_count(
                [('partner_id', '=', self.partner_id.id)])

    def action_get_vehicles_record(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Vehicles',
            'view_mode': 'tree',
            'res_model': 'vehicle.management',
            'domain': [('partner_id', '=', self.partner_id.id)],
            'context': "{'create': False}"
        }

    @api.onchange('duration_time')
    def calculate_delivery_date(self):
        print(self.partner_id.mapped('active'))
        if self.duration_time:
            self.delivery_date = self.start_date + timedelta(days=self.duration_time)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', _('New')) == _('New'):
                vals['name'] = self.env['ir.sequence'].next_by_code('vehicle.reference')
        return super().create(vals_list)

    def confirm_button(self):
        self.write({
            'state': "progress"
        })

    def ready_to_delivery(self):
        self.write({
            'state': "ready for delivery"
        })

    @api.constrains('vehicle_number', 'start_date', 'partner_id')
    def _check_vehicle_unique(self):
        for record in self:
            existing_vehicle = self.search([
                ('vehicle_number', '=', record.vehicle_number),
                ('start_date', '=', record.start_date),
                ('partner_id', '=', record.partner_id.id),
            ])
            print(existing_vehicle)
            if len(existing_vehicle) > 1:
                raise ValidationError('This Vehicle number is invalid.')

    @api.onchange('product_line_ids')
    def _total_product_cost(self):
        self.total_product_cost = sum(self.product_line_ids.mapped('product_sub_total'))

    @api.onchange('labour_line_ids')
    def _total_time_product_cost(self):
        print(self.labour_line_ids.mapped('sub_total_time_cost'))
        self.total_time_cost = sum(self.labour_line_ids.mapped('sub_total_time_cost'))

    @api.onchange('total_time_cost', 'total_product_cost')
    def _total_cost(self):
        self.total_cost = self.total_time_cost + self.total_product_cost

    def action_create_invoice(self):
        print(self.product_line_ids.product_id)
        invoice_vals = {
            'partner_id': self.partner_id.id,
            'move_type': 'out_invoice',
            'invoice_date': fields.Date.today(),
            'invoice_line_ids': [(0, 0, {
                'product_id': self.product_line_ids.product_id.id,
                'name': self.vehicle_number,
                'quantity': self.product_line_ids.quantity,
                'price_unit': self.product_line_ids.product_price,
            })],
        }
        invoice = self.env['account.move'].create(invoice_vals)

        return {
            'type': 'ir.actions.act_window',
            'name': 'Customer Invoice',
            'res_model': 'account.move',
            'res_id': invoice.id,
            'view_mode': 'form',
            'view_id': self.env.ref('account.view_move_form').id,
            'target': 'current',
        }

