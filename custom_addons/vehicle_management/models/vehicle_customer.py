# -*- coding: utf-8 -*-

from odoo import api, fields, models


class VehicleCustomer(models.Model):
    _inherit = 'res.partner'

    smart_partner = fields.Integer(compute='vehicle_history')

    def vehicle_history(self):
        for record in self:
            record.smart_partner = self.env['vehicle.management'].search_count(
                [('partner_id', 'in', self.ids)])

    def action_get_vehicles_record(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Vehicles',
            'view_mode': 'tree',
            'res_model': 'vehicle.management',
            'domain': [('partner_id', '=', self.ids)],
            'context': "{'create': False}"
        }


