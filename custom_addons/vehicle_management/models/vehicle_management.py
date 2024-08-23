# -*- coding: utf-8 -*-

import datetime

from datetime import timedelta

from odoo import api, Command, fields, models, _

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
                                      related='vehicle_id.category_id', store=True, ondelete='set null')
    active = fields.Boolean(default=True)
    state = fields.Selection(selection=[('draft', 'Draft'),
                                        ('progress', 'Progress'),
                                        ('ready for delivery', 'Ready For Delivery'),
                                        ('done', 'Done'),
                                        ('cancelled', 'Cancelled'),
                                        ('paid', 'Paid')],
                             default='draft', required=True, tracking=True, compute="_compute_ready_for_delivery",
                             store=True)
    phone = fields.Char(related='partner_id.phone', string="Phone", readonly=False)
    vehicle_number = fields.Char(string="Vehicle number", copy=False, required=True)
    image = fields.Image(string="Image")
    start_date = fields.Date('Start Date',
                             required=True,
                             default=fields.Date.today())
    duration_time = fields.Integer(string="Duration")
    delivery_date = fields.Date(string="Delivery date", readonly=True)
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
    total_product_cost = fields.Monetary(string="Total cost", readonly=True, default=0.0,
                                         compute="_compute_total_product_cost")
    total_time_cost = fields.Monetary(string="Total cost", readonly=True, default=0.0,
                                      compute="_compute_total_time_cost")
    total_cost = fields.Monetary(string="Total cost", default=0.0)
    estimated_delivery_date = fields.Date(string="Estimated delivery date")
    smart_invoice = fields.Integer(compute='compute_invoice_count')
    invoice_id = fields.Many2one('account.move', string="Invoice", store=True)
    invoice_status = fields.Selection(related='invoice_id.state')
    paid_status = fields.Char(compute="_compute_change_payment_state")
    color_change = fields.Char(string="Color", default=0, store=True)

    def compute_invoice_count(self):
        """ To count the number of invoice of a customer on a vehicle service form to set inside the smart button"""
        self.smart_invoice = len(self.invoice_id)

    def action_get_invoice_record(self):
        """ To return a form view of invoice while clicking the smart button inside the service form """
        if self.invoice_id:
            return {
                'type': 'ir.actions.act_window',
                'res_model': 'account.move',
                'res_id': self.invoice_id.id,
                'view_mode': 'form',
                'view_id': self.env.ref('account.view_move_form').id,
            }

    def calculate_delivery_date(self):
        """ To set the delivery date inside the delivery_date field and change the state to 'done' while clicking the
            done button"""
        self.delivery_date = datetime.date.today()
        self.write({
            'state': 'done'
        })

    @api.model_create_multi
    def create(self, vals_list):
        """ To create vehicle service form sequence """
        for vals in vals_list:
            if vals.get('name', _('New')) == _('New'):
                vals['name'] = self.env['ir.sequence'].next_by_code('vehicle.reference')
        return super().create(vals_list)

    def action_confirm_button(self):
        """ to change the state of vehicle service form to 'progress' while clicking the 'confirm' button"""
        self.write({
            'state': "progress"
        })

    def action_ready_to_delivery(self):
        """ to change the state of vehicle service form to 'ready for delivery' while clicking the
        'ready for delivery button' button"""
        self.write({
            'state': "ready for delivery"
        })

    def action_to_cancel(self):
        """ to change the state of vehicle service form to 'cancelled' while clicking the 'confirm' button"""
        self.write({
            'state': "cancelled"
        })

    def action_move_to_draft(self):
        """ to change the state of vehicle service form to 'draft' while clicking the 'move to draft' button"""
        self.write({
            'state': "draft"
        })

    @api.constrains('vehicle_number', 'start_date', 'partner_id')
    def _check_vehicle_unique(self):
        """ To check the vehicle number is unique based on customer and start_date"""
        for record in self:
            existing_vehicle = self.search([
                ('vehicle_number', '=', record.vehicle_number),
                ('start_date', '=', record.start_date),
                ('partner_id', '=', record.partner_id.id),
            ])
            print(existing_vehicle)
            if len(existing_vehicle) > 1:
                raise ValidationError('This Vehicle number is invalid.')

    @api.depends('product_line_ids')
    def _compute_total_product_cost(self):
        """ To compute the vehicle product total cost """
        self.total_product_cost = sum(self.product_line_ids.mapped('product_sub_total'))

    @api.depends('labour_line_ids')
    def _compute_total_time_cost(self):
        """ To compute the labour total cost """
        self.total_time_cost = sum(self.labour_line_ids.mapped('sub_total_time_cost'))

    @api.onchange('total_time_cost', 'total_product_cost')
    def _total_cost(self):
        """ To compute the total cost
             total_cost = total_time_cost + total_product_cost """
        self.total_cost = self.total_time_cost + self.total_product_cost

    def action_create_invoice(self):
        """ To create a new invoice for the customer and if the invoice is not paid while creating the invoice  again
        for that particular customer the products in the new service form will append with the existing invoice  """
        existing_invoice = self.env['account.move'].search([
                ('partner_id', '=', self.partner_id.id),
                ('move_type', '=', 'out_invoice'),
                ('payment_state', '!=', 'paid'),
            ], limit=1)
        invoice_vals = []
        if existing_invoice:
            for record in self.product_line_ids:
                invoice_vals.append(Command.create({'product_id': record.product_id.id,
                                                    'price_unit': record.product_price,
                                                    'quantity': record.quantity,
                                                    }))
            for record in self.labour_line_ids:
                invoice_vals.append(Command.create({'product_id':
                                                    self.env.ref('vehicle_management.vehicle_labour_product_product').id,
                                                    'name': record.labor_id.name,
                                                    'price_unit': record.hourly_cost,
                                                    'quantity': record.time_spent,
                                                    }))
            existing_invoice.write({
                'invoice_line_ids': invoice_vals
            })
            self.invoice_id = existing_invoice.id

            return {
              'type': 'ir.actions.act_window',
              'name': 'Customer Invoice',
              'res_model': 'account.move',
              'res_id': existing_invoice.id,
              'view_mode': 'form',
              'view_id': self.env.ref('account.view_move_form').id,
            }

        else:
            invoice_vals = []
            for record in self.product_line_ids:
                invoice_vals.append(Command.create({'product_id': record.product_id.id,
                                                    'price_unit': record.product_price,
                                                    'quantity': record.quantity,
                                                    }))
            for record in self.labour_line_ids:
                invoice_vals.append(Command.create({'product_id':
                                                    self.env.ref('vehicle_management.vehicle_labour_product_product').id,
                                                    'name': record.labor_id.name,
                                                    'price_unit': record.hourly_cost,
                                                    'quantity': record.time_spent,
                                                    }))

            out_invoice = self.env['account.move'].create({
              'move_type': 'out_invoice',
              'date': datetime.date.today(),
              'invoice_date': datetime.date.today(),
              'partner_id': self.partner_id.id,
              'invoice_line_ids': invoice_vals
              })
            self.invoice_id = out_invoice.id

            return {
              'type': 'ir.actions.act_window',
              'name': 'Customer Invoice',
              'res_model': 'account.move',
              'res_id': out_invoice.id,
              'view_mode': 'form',
              'view_id': self.env.ref('account.view_move_form').id,
            }

    def _compute_change_payment_state(self):
        """ To change the state of the service form to 'paid' while changing the payment state of the invoice to
            'paid'"""
        self.paid_status = self.invoice_id.payment_state
        if self.paid_status == 'paid':
            self.write({
                'state': "paid"
                })

    @api.constrains('state')
    def _compute_ready_for_delivery(self):
        """ To call the action_send_mail while changing the state of the service form to 'ready for delivery'"""
        if self.state == 'ready for delivery':
            self.action_send_mail()

    def action_send_mail(self):
        """ To send the email to customer"""
        mail_template = self.env.ref("vehicle_management.vehicle_delivery_mail_template")
        mail_template.send_mail(self.id, force_send=True)

    def vehicle_form_archive(self):
        """ For scheduled action, if the service form is in the 'cancelled' state for 1 month it will automatically
            archive"""
        for record in self.search([('state', '=', 'cancelled'),
                                   ('start_date', '<=', datetime.date.today() - datetime.timedelta(30))]):
            record.action_archive()

    def update_customer_stage(self):
        """Function for automation rule to change the customer state"""
        for record in self.env['vehicle.management'].search([('partner_id', '=', self.id)]):
            record.customer_state = 'service customer'

    def vehicle_record_color_change(self):
        """ For scheduled action, if the estimated delivery date is today and the state is in progress
        change the record color to red, if it's tomorrow then orange"""
        for today_delivery in self.search([('estimated_delivery_date', '=', datetime.date.today()),
                                           ('state', '=', 'progress')]):
            if today_delivery:
                today_delivery.color_change = 'red'

        for tomorrow_delivery in self.search([('estimated_delivery_date', '=', datetime.date.today() + datetime.timedelta(1)),
                                              ('state', '=', 'progress')]):
            if tomorrow_delivery:
                tomorrow_delivery.color_change = 'orange'
