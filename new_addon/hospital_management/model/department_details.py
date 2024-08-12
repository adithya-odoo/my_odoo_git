from odoo import models, fields


class DepartmentDetails(models.Model):
    _inherit = "hr.department"

    name = fields.Char()
    block_number = fields.Integer()
    doctor = fields.Many2one('hr.employee', "Doctor")

