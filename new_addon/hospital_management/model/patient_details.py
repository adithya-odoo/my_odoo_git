from odoo import models, fields


class PatientsDetails(models.Model):
    _inherit = 'res.partner'

    name = fields.Char(required=True)
    age = fields.Integer()
    blood_group = fields.Selection([('O+', 'O+'), ('A+', 'A+'), ('B+', 'B+'), ('AB+', 'AB+'), ('O-', 'O-')])
