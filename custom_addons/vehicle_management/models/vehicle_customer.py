# -*- coding: utf-8 -*-

from odoo import fields, models


class VehicleCustomer(models.Model):
    _inherit = 'res.partner'

    smart_partner = fields.Integer(compute='_compute_vehicle_history')
    customer_state = fields.Selection(selection=[('non service customer', 'Non service customer'),
                                                 ('service customer', 'Service customer')],
                                      default='non service customer', string="Customer State")

    def _compute_vehicle_history(self):
        """
         To compute the number of vehicle number of a customer to set inside the smart button
         """
        self.smart_partner = self.env['vehicle.management'].search_count([('partner_id', 'in', self.ids)])

    def action_get_vehicles_record(self):
        """
         To return the tree view while clicking the smart button
         """
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Vehicles',
            'view_mode': 'tree',
            'res_model': 'vehicle.management',
            'domain': [('partner_id', '=', self.ids)],
            'context': "{'create': False}"
        }

    def action_archive(self):
        """
         To archive the vehicle service form while archiving the customer
         """
        res = super().action_archive()
        vehicle_customer = self.env['vehicle.management'].search([('partner_id', '=', self.id)])
        if vehicle_customer:
            vehicle_customer.action_archive()
        return res

    def action_unarchive(self):
        """
        To unarchive the vehicle service form while archiving the customer
        """
        res = super().action_unarchive()
        vehicle_customer = self.env['vehicle.management'].search([('partner_id', '=', self.id),
                                                                  ('active', '=', False)])
        if vehicle_customer:
            vehicle_customer.action_unarchive()
        return res

    def get_vehicle_management_form_view(self):
        """
        To get the vehicle service form while clicking the 'create service form' button inside partner form
        """
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'vehicle.management',
            'view_mode': 'form',
            'view_id': self.env.ref('vehicle_management.vehicle_management_form_view').id,
        }

