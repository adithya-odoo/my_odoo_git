# -*- coding: utf-8 -*-
import datetime

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
    estimated_delivery_date = fields.Date(string="Estimated delivery date")
    smart_invoice = fields.Integer(compute='compute_invoice_count')
    invoice_id = fields.Many2one('account.move', string="Invoice", store=True)
    invoice_status = fields.Selection(related='invoice_id.state')
    paid_status = fields.Char(compute="change_payment_state")

    def compute_invoice_count(self):
        for record in self:
            record.smart_invoice = len(record.invoice_id)

    def action_get_invoice_record(self):
        if self.invoice_id:
            return {
                'type': 'ir.actions.act_window',
                'res_model': 'account.move',
                'res_id': self.invoice_id.id,
                'view_mode': 'form',
                'view_id': self.env.ref('account.view_move_form').id,
            }

    def calculate_delivery_date(self):
        self.delivery_date = datetime.date.today()
        self.write({
            'state': 'done'
        })

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
            if len(existing_vehicle) > 1:
                raise ValidationError('This Vehicle number is invalid.')

    @api.onchange('product_line_ids')
    def _total_product_cost(self):
        self.total_product_cost = sum(self.product_line_ids.mapped('product_sub_total'))

    @api.onchange('labour_line_ids')
    def _total_time_product_cost(self):
        self.total_time_cost = sum(self.labour_line_ids.mapped('sub_total_time_cost'))

    @api.onchange('total_time_cost', 'total_product_cost')
    def _total_cost(self):
        self.total_cost = self.total_time_cost + self.total_product_cost

    def action_create_invoice(self):
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
                invoice_vals.append(Command.create({'product_id': self.env.ref('vehicle_management.vehicle_labour_product_product').id,
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
                invoice_vals.append(Command.create({'product_id': self.env.ref('vehicle_management.vehicle_labour_product_product').id,
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

    def change_payment_state(self):
        for record in self:
            record.paid_status = record.invoice_id.payment_state
            if record.paid_status == 'paid':
                record.write({
                    'state': "paid"
                })

    @api.onchange('state')
    def check_ready_for_delivery(self):
        if self.state == 'ready for delivery':
            self.action_send_mail()

    def action_send_mail(self):
        mail_template = self.env.ref("vehicle_management.mail_template_blog")
        mail_template.send_mail(self.id, force_send=True)

    def vehicle_form_archive(self):
        for record in self.search([('state', '=', 'cancelled'),
                                   ('start_date', '<=', datetime.date.today() - datetime.timedelta(30))]):
            record.action_archive()

    # def customer_archive(self):
    #     archived_customer = self.env['res.partner'].search([('active', '=', False)])
    #     res = super().action_archive()




