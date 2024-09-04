# -*- coding: utf-8 -*-
import json

import io

from gevent.testing.testrunner import report

from odoo import fields, models

from odoo.tools import date_utils

from odoo.exceptions import ValidationError

from odoo.tools.misc import xlsxwriter


class ReportFilter(models.TransientModel):
   """This model is used to pop up a report filter."""
   _name = 'report.filter'
   _description = "Filter Wizard"

   start_date = fields.Date(string="Start date")
   end_date = fields.Date(string="End date")
   customer_ids = fields.Many2many('res.partner', string="Customer")
   advisor_ids = fields.Many2many('res.users', string="Advisor")

   def action_print_report_pdf(self):
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

   def print_xlsx(self):
      if self.start_date > self.end_date:
         raise ValidationError('Start Date must be less than End Date')
      excel_data = {
         'start_date': self.start_date,
         'end_date': self.end_date,
      }
      for rec in self.customer_ids:
         excel_data.setdefault('customer_ids', [])
         excel_data['customer_ids'].append(rec.id)

      for rec in self.advisor_ids:
         excel_data.setdefault('advisor_ids', [])
         excel_data['advisor_ids'].append(rec.id)

      if self.advisor_ids:
         excel_data['advisor_len'] = len(excel_data['advisor_ids'])
      if self.customer_ids:
         excel_data['customer_len'] = len(excel_data['customer_ids'])

      print(excel_data)
      return {
         'type': 'ir.actions.report',
         'data': {'model': 'report.filter',
                  'options': json.dumps(excel_data,
                                        default=date_utils.json_default),
                  'output_format': 'xlsx',
                  'report_name': 'Excel Report',
                  },
         'report_type': 'xlsx',
      }

   def get_xlsx_report(self, excel_data, response):
      """ To generate Excel sheet through JS"""
      query = """ select model.name as vehicle_name, partner.name as customer_name,
                           users.name as advisor, vm.vehicle_number as vehicle_number, cat.name as cat,
      					 upper(vm.state) as state, upper(vm.service_type) as service_type , vm.total_cost as cost,
      					 vm.estimated_amount as estimated_amount from vehicle_management as vm
                           inner join res_partner as partner on partner.id = vm.partner_id
                           inner join fleet_vehicle_model as model on  model.id = vm.vehicle_id
      				     inner join fleet_vehicle_model_category as cat on cat.id = vm.vehicle_type_id
      					 inner join res_partner as users on users.id =  (select partner_id from res_users where id = advisor_id)"""

      if excel_data.get('start_date') and excel_data.get('end_date'):
         query += """ where start_date between '%s' and '%s' """ % (
         excel_data.get('start_date'), (excel_data.get('end_date')))
      if excel_data.get('customer_ids'):
         query += """ and partner_id in %s """ % (
            str(tuple(excel_data.get('customer_ids')))).replace(",)", ")")
      if excel_data.get('advisor_ids'):
         query += """ and advisor_id in %s """ % (
            str(tuple(excel_data.get('advisor_ids')))).replace(",)", ")")

      self.env.cr.execute(query)
      data = self.env.cr.dictfetchall()

      for record in data:
         record['advisor_len'] = 0
         record['customer_len'] = 0

      if excel_data.get('advisor_ids'):
         for record in data:
            record['advisor_len'] = excel_data.get('advisor_len')
      if excel_data.get('customer_ids'):
         for record in data:
            record['customer_len'] = excel_data.get('customer_len')

      print(data,"EWFEDE")

      output = io.BytesIO()
      workbook = xlsxwriter.Workbook(output, {'in_memory': True})
      sheet = workbook.add_worksheet()
      cell_format = workbook.add_format(
         {'font_size': '10px', 'align': 'center', 'bold': True})
      head = workbook.add_format(
         {'align': 'center', 'bold': True, 'font_size': '20px'})
      txt = workbook.add_format({'font_size': '10px', 'align': 'center'})
      sheet.merge_range('F2:K3', 'VEHICLE MANAGEMENT', head)
      sheet.merge_range('A6:B6', 'Vehicle name', cell_format)
      sheet.merge_range('C6:D6', 'vehicle number', cell_format)
      sheet.merge_range('E6:F6', 'Advisor', cell_format)
      sheet.merge_range('G6:H6', 'Customer name', cell_format)
      sheet.write('I6', 'Category', cell_format)
      sheet.write('J6', 'State', cell_format)
      sheet.merge_range('K6:L6', 'Service Type', cell_format)
      sheet.write('M6', 'Cost', cell_format)
      sheet.merge_range('N6:O6', 'Estimated Amount', cell_format)

      for rec in data:
         print(rec.get('vehicle_name'))
         sheet.merge_range('A7:B7', rec.get('vehicle_name'), txt)
         sheet.merge_range('C7:D7', rec['vehicle_number'], txt)
         sheet.merge_range('E7:F7', rec['advisor'], txt)
         sheet.merge_range('G7:H7', rec['customer_name'], txt)
         sheet.write('I7', rec['cat'], txt)
         sheet.write('J7', rec['state'], txt)
         sheet.merge_range('K7:L7', rec['service_type'], txt)
         sheet.write('M7',rec['cost'], txt)
         sheet.merge_range('N7:O7', rec['estimated_amount'], txt)

      workbook.close()
      output.seek(0)
      response.stream.write(output.read())
      output.close()
