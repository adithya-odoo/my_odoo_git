# -*- coding: utf-8 -*-

from odoo.http import request, Controller, route, Response
import random


class DynamicSnippets(Controller):
   """This class is for the getting values for dynamic product snippets
      """
   @route('/repair-snippet', type='json', auth='public', website=True, methods=['POST'])
   def repair_order(self):
       """Function for getting the current website and last 4 repair order"""
       repair_orders = request.env['vehicle.management'].sudo().search_read([], ['name', 'image',
                                                                                 'vehicle_id',
                                                                                 'vehicle_number'],
                                                                            order='create_date DESC')

       print(repair_orders, "controller")
       return repair_orders