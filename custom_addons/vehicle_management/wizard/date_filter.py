# -*- coding: utf-8 -*-

from odoo import fields, models

from odoo.exceptions import ValidationError


class DateFilter(models.TransientModel):
   """This model is used to pop up a report filter."""
   _name = 'date.filter'
   _description = "Filter Wizard"

   start_date = fields.Date(string="Start date")
   end_date = fields.Date(string="End date")
   customer_ids = fields.Many2many('res.partner', string="Customer")
   advisor_ids = fields.Many2many('res.users', string="Advisor")

   def action_print_date_pdf(self):
      if self.start_date and self.end_date:
         if self.start_date > self.end_date:
            raise ValidationError('End date should be larger than start date')

      data = {
            'end_date': self.end_date,
            'start_date': self.start_date,
         }
      for rec in self.customer_ids:
         data.setdefault('customer_ids', [])
         data['customer_ids'].append(rec.id)

      for rec in self.advisor_ids:
         data.setdefault('advisor_ids', [])
         data['advisor_ids'].append(rec.id)

      if self.advisor_ids:
         data['advisor_len'] = len(data['advisor_ids'])
      if self.customer_ids:
         data['customer_len'] = len(data['customer_ids'])

      print(data)

      return (self.env.ref(
         'vehicle_management.action_report_vehicle_management').report_action(None, data=data))

