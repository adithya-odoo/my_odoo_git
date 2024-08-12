from odoo import fields, models, _, api


class OpTicket(models.Model):
    _name = "op.ticket"
    _description = "Op ticket"

    name = fields.Char('Reference', default=lambda self: _('New'), copy=False, readonly=True, tracking=True)
    token_number = fields.Integer()
    patient_name = fields.Many2one('res.partner', 'patient')
    doctor = fields.Many2one('hr.employee', "Doctor")
    age = fields.Integer()
    date = fields.Date()
    department = fields.Many2one('hr.department', "Department")
    state = fields.Selection(selection=[('draft', 'Draft'), ('done', 'Done'),], string='Status', required=True, readonly=True, copy=False, tracking=True, default='draft')

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', _('New')) == _('New'):
                vals['name'] = self.env['ir.sequence'].next_by_code('op.ticket.Reference')
        return super().create(vals_list)

    @api.onchange('patient_name')
    def onchange_patient_name(self):
        self.age = self.patient_name.age

    @api.onchange('doctor')
    def onchange_doctor_name(self):
        self.department = self.doctor.department_id

    def confirm_button(self):
        self.write({
            'state': "done"
        })

