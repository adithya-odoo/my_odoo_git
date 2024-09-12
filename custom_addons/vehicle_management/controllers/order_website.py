# -*- coding: utf-8 -*-

from odoo.http import request, Controller, route

from odoo.models import check_method_name

from odoo.api import call_kw

import base64


class WebFormController(Controller):
    """ Web site controller To post value to database and to pass value to js"""
    def _call_kw(self, model, method, args, kwargs):
        """to call_kw function"""
        check_method_name(method)
        return call_kw(request.env[model], method, args, kwargs)

    @route(['/web/dataset/call_kw', '/web/dataset/call_kw/<path:path>'], type='json', auth="public")
    def call_kw(self, model, method, args, kwargs, path=None):
        """To call _call_kw function"""
        return self._call_kw(model, method, args, kwargs)

    @route('/repairform', auth='public', website=True)
    def web_form(self, **kwargs):
        """ To pass value to the Xml file of website template"""
        values ={
          'partner' :  request.env['res.partner'].sudo().search([]),
          'users': request.env['res.users'].sudo().search([]),
          'vehicle_type': request.env['fleet.vehicle.model.category'].sudo().search([]),
          'vehicle_name' : request.env['fleet.vehicle.model'].sudo().search([]),
          'country': request.env['res.country'].sudo().search([])
        }
        return request.render('vehicle_management.repair_web_form_template', values)

    @route('/repairform/submit', type='http', auth='public', website=True, methods=['POST'])
    def web_form_submit(self, **post):
        """ To post value to the database and create data in 'vehicle.management'
         while click the submit button"""
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


    @route('/customerform/submit', type='http', auth='public', website=True, methods=['POST'])
    def customer_form_submit(self, **post):
        """ To post value to the database and create data in 'res.partner'
                while click the submit button"""
        print("hello", post.get('img'))
        request.env['res.partner'].sudo().create({
            'name': post.get('name'),
            'email': post.get('email'),
            'phone': post.get('phone'),
            'street':post.get('street1'),
            'street2':post.get('street2'),
            'city':post.get('city'),
            'country_id':post.get('country_field'),
            'image_1920':  base64.b64encode(post.get('img').read()),
        })
        return request.redirect('/repairform')
