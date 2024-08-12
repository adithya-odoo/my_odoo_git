from odoo import models, fields


class HospitalMedicine(models.Model):
    _name = "hospital.medicine"
    _description = "Hospital Medicine"

    name = fields.Char()
    rate = fields.Float()
