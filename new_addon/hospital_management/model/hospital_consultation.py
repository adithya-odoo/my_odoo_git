from odoo import models, fields, api


class Consulting(models.Model):
    _name = "hospital.consultation"
    _description = "Hospital consultation"

    doctor = fields.Many2one('res.partner', "Doctor")
    patient = fields.Many2one('res.partner', "Patient")
    date = fields.Datetime(default=fields.Datetime.now())
    op_number = fields.Many2one('op.ticket', string="Op number")

    @api.onchange('op_number')
    def op_number_change(self):
        self.doctor = self.op_number.doctor
        self.patient = self.op_number.patient_name
        print(self.op_number.doctor)

