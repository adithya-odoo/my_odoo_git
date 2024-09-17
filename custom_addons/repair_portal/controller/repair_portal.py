# -*- coding: utf-8 -*-

from odoo.http import content_disposition, Controller, request, route

from odoo import _

from odoo.addons.portal.controllers.portal import CustomerPortal

from odoo.addons.portal.controllers.portal import pager as portal_pager


class PortalRepair(CustomerPortal):
   def _prepare_home_portal_values(self, counters):
       print("port")
       values = super()._prepare_home_portal_values(counters)
       user = request.env.user.partner_id
       if 'repair_count' in counters:
           repair_count = request.env['vehicle.management'].search_count(
               [('partner_id', '=', user.id)])
           values['repair_count'] = repair_count
       return values

   def _get_repair_searchbar_sortings(self):
       return {
           'date': {'label': _('Order Date'), 'order': 'start_date desc'},
           'name': {'label': _('Reference'), 'order': 'name'},
           'stage': {'label': _('Stage'), 'order': 'state'},
       }
   def _prepare_repair_portal_rendering_values(self, page=1, sortby=None, **kwargs):
       repair_order = request.env['vehicle.management']
       print(repair_order)
       if not sortby:
           sortby = 'date'

       user = request.env.user.partner_id
       values = self._prepare_portal_layout_values()

       searchbar_sortings = self._get_repair_searchbar_sortings()

       sort_order = searchbar_sortings[sortby]['order']
       url = '/my/repair'
       domain = [('partner_id', '=', user.id)]

       pager_values = portal_pager(
           url= url,
           total=repair_order.search_count(domain),
           page=page,
           step=self._items_per_page,
           url_args={'sortby': sortby},
       )
       repair = repair_order.search(domain, order=sort_order,
                                 limit=self._items_per_page,
                                 offset=pager_values['offset'])
       print(repair)

       values.update({
           'repair':repair.sudo(),
           'page_name': 'Repair Order',
           'pager': pager_values,
           'default_url': url,
           'searchbar_sortings': searchbar_sortings,
           'sortby': sortby,
        })

       return values

   @route('/my/repair', type='http', auth="user", website=True)
   def portal_repair(self, **kwargs):
       values = self._prepare_repair_portal_rendering_values(**kwargs)
       return request.render("repair_portal.portal_repair", values)

