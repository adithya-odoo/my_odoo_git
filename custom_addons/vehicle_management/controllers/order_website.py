# -*- coding: utf-8 -*-

from odoo.http import request, Controller, route
import base64


class WebFormController(Controller):

    @route('/repairform', auth='public', website=True)
    def web_form(self, **kwargs):
        print("web_form")
        values ={
          'partner' :  request.env['res.partner'].sudo().search([]),
          'users': request.env['res.users'].sudo().search([]),
          'vehicle_type': request.env['fleet.vehicle.model.category'].sudo().search([]),
          # 'vehicle_name' : request.env['fleet.vehicle.model'].sudo().search([]),
        }

        return request.render('vehicle_management.repair_web_form_template', values)

    @route('/repairform/submit', type='http', auth='public', website=True, methods=['POST'])
    def web_form_submit(self, **post):
        print("hello")
        print(post)
        request.env['vehicle.management'].sudo().create({
                    'partner_id': post.get('partner_field'),
                    'advisor_id':post.get('users_field'),
                    'vehicle_type_id':post.get('vehicle_type_field'),
                    'vehicle_id':post.get('vehicle_field'),
                    'phone': post.get('phone'),
                    'vehicle_number': post.get('vehicle_number'),
                    'image' : base64.b64encode(post.get('image').read())
                })
        return request.redirect('/repairform-thank-you')
