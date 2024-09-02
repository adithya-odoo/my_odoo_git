# -*- coding: utf-8 -*-

from odoo import fields, models


class DateFilter(models.TransientModel):
   """This model is used to pop up a report filter."""
   _name = 'date.filter'
   _description = "Filter Wizard"

   start_date = fields.Date(string="Start date")
   end_date = fields.Date(string="End date")
   customer_ids = fields.Many2many('res.partner', string="Customer")
   advisor_ids = fields.Many2many('res.users', string="Advisor")

   def action_print_date_pdf(self):
      # vehicle_management = self.env['vehicle.management'].search([('is_active', '=', True)])
      print(self.start_date)
      print(self.end_date)

      data = {
         'end_date': self.end_date,
         'start_date': self.start_date,
         'advisor_ids': self.advisor_ids,
         'customer_ids':self.customer_ids,
      }

      return (self.env.ref(
         'vehicle_management.action_report_vehicle_management').report_action(None, data=data))
