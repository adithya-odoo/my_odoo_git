# -*- coding: utf-8 -*-
import json

import io
from re import search

import html2text

from odoo import fields, models

from odoo.tools import date_utils

from odoo.exceptions import ValidationError

from odoo.tools.misc import xlsxwriter

from odoo.tools.safe_eval import datetime


class ReportFilter(models.TransientModel):
   """This model is used to pop up a report filter."""
   _name = 'report.filter'
   _description = "Filter Wizard"

   start_date = fields.Date(string="Start date")
   end_date = fields.Date(string="End date")
   customer_ids = fields.Many2many('res.partner', string="Customer")
   advisor_ids = fields.Many2many('res.users', string="Advisor")

   def action_print_report_pdf(self):
      print("action_print_report_pdf")
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
      """ To generate EXCEL report while click the Print Excel button"""
      if self.start_date and self.end_date:
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
      					 vm.state as state, vm.service_type as service_type , vm.total_cost as cost,
      					 vm.estimated_amount as estimated_amount from vehicle_management as vm
                         inner join res_partner as partner on partner.id = vm.partner_id
                         inner join fleet_vehicle_model as model on  model.id = vm.vehicle_id
      				     inner join fleet_vehicle_model_category as cat on cat.id = vm.vehicle_type_id
      					 inner join res_partner as users on users.id =  (select partner_id from res_users where id = advisor_id)"""

      if excel_data.get('start_date'):
         if excel_data.get('start_date') and excel_data.get('end_date'):
            query += """ where start_date between '%s' and '%s' """ % (
               excel_data.get('start_date'), (excel_data.get('end_date')))
         else:
            query += """ where start_date >= '%s' """ %(excel_data.get('start_date'))

      if excel_data.get('end_date'):
         if excel_data.get('start_date') and excel_data.get('end_date'):
            query += """ where start_date between '%s' and '%s' """ % (
               excel_data.get('start_date'), (excel_data.get('end_date')))
         else:
            query += """ where start_date <= '%s'""" %(excel_data.get('end_date'))

      if excel_data.get('customer_ids'):
         query += """ and partner_id in %s """ % (
            str(tuple(excel_data.get('customer_ids')))).replace(",)", ")")
      if excel_data.get('advisor_ids'):
         query += """ and advisor_id in %s """ % (
            str(tuple(excel_data.get('advisor_ids')))).replace(",)", ")")

      self.env.cr.execute(query)
      excel = self.env.cr.dictfetchall()

      print(query)
      print(excel)

      for record in excel:
         record['advisor_len'] = 0
         record['customer_len'] = 0
         record['vehicle_name'] = record.get('vehicle_name').capitalize()
         record['service_type'] = record.get('service_type').capitalize()

      state_dict = dict(self.env['vehicle.management']._fields['state'].selection)

      if excel_data.get('advisor_ids'):
         for record in excel:
            record['advisor_len'] = excel_data.get('advisor_len')
      if excel_data.get('customer_ids'):
         for record in excel:
            record['customer_len'] = excel_data.get('customer_len')

      output = io.BytesIO()
      workbook = xlsxwriter.Workbook(output, {'in_memory': True})
      sheet = workbook.add_worksheet()
      cell_format = workbook.add_format(
         {'font_size': '10px', 'align': 'center', 'bold': True})
      details = workbook.add_format(
         {'font_size': '10px', 'align': 'top', 'bold': True})
      head = workbook.add_format(
         {'align': 'center', 'bold': True, 'font_size': '20px'})
      print(html2text.html2text(self.env.company.company_details))
      txt = workbook.add_format({'font_size': '10px', 'align': 'center'})
      # Sheet heading
      cur = self.env.company.currency_id.symbol
      print(cur)
      sheet.merge_range('D3:G4', 'VEHICLE MANAGEMENT', head)
      sheet.write('I1',str(datetime.date.today()), cell_format)
      sheet.merge_range('A1:C3',html2text.html2text(self.env.company.company_details), details)
      sheet.merge_range('A4:B4',self.env.company.email,details)
      sheet.set_column(0,9,13)
      sheet.set_row(0,20)
      #Table data
      row = 6
      for rec in excel:
         column = 0
         # insert data near heading if it's lesser than 2
         if rec['advisor_len'] < 2 and rec['advisor_len'] != 0:
            sheet.write('A4',"Advisor:", cell_format)
            sheet.merge_range('B4:C4', rec['advisor'], txt)
         if rec['customer_len'] < 2 and rec['customer_len'] != 0:
            print("cust")
            sheet.write('A5',"Customer:", cell_format)
            sheet.merge_range('B5:C5', rec['customer_name'], txt)

         # table data
         sheet.write(5, column, 'Vehicle', cell_format)
         sheet.write(row,column, rec.get('vehicle_name'), txt)
         column += 1
         print(column)

            # Hiding column if the data is lesser than 1
         if rec['advisor_len'] > 1 or rec['advisor_len'] == 0:
             sheet.write(5, column, 'Advisor', cell_format)  # Table heading
             sheet.write(row, column, rec['advisor'], txt)  # Table data
             column += 1

         if rec['customer_len'] > 1 or rec['customer_len'] == 0:
             sheet.write(5, column,'Customer', cell_format)  # Table heading
             sheet.write(row, column, rec['customer_name'], txt)  # Table data
             column +=1

         sheet.write(5, column, 'vehicle number', cell_format)
         sheet.write(row,column, rec['vehicle_number'], txt)
         column += 1
         sheet.write(5, column, 'Category', cell_format)
         sheet.write(row,column, rec['cat'], txt)
         column += 1
         sheet.write(5, column, 'State', cell_format)
         sheet.write(row,column, state_dict[rec['state']], txt)
         column += 1
         sheet.write(5, column, 'Service Type', cell_format)
         sheet.write(row,column, rec['service_type'], txt)
         column += 1
         sheet.write(5, column, 'Cost', cell_format)
         sheet.write(row,column, cur+str(rec['cost']), txt)
         column += 1
         sheet.write(5, column, 'Estimated Amount', cell_format)
         sheet.write(row,column, cur+str(rec['estimated_amount']), txt)
         column += 1
         row += 1

      workbook.close()
      output.seek(0)
      response.stream.write(output.read())
      output.close()

