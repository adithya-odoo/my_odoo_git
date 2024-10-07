# -*- coding: utf-8 -*-

from odoo import api, models


class CrmLead(models.Model):
    """crm inherited model"""
    _inherit = 'crm.lead'


    @api.model
    def get_tiles_data(self):
        """ Return the tile data"""
        company_id = self.env.company
        leads = self.search([('company_id', '=', company_id.id),
                             ('user_id', '=', self.env.user.id)])
        lost = self.search_read([('company_id', '=', company_id.id),
                             ('user_id', '=', self.env.user.id),
                             ('active', '=',  False)])

        my_leads = leads.filtered(lambda r: r.type == 'lead')
        my_opportunity = leads.filtered(lambda r: r.type == 'opportunity')
        sale_order = 0
        for i in my_opportunity.order_ids:
            sale_order += self.env['sale.order'].browse(i.ids).amount_invoiced
        won = leads.filtered(lambda r:r.stage_id.id == 4)
        currency = company_id.currency_id.symbol
        expected_revenue = sum(my_opportunity.mapped('expected_revenue'))
        return {
            'total_leads': len(my_leads),
            'total_opportunity': len(my_opportunity),
            'expected_revenue': expected_revenue,
            'won' : len(won),
            'lost': len(lost),
            'currency': currency,
            'invoiced_amount': sale_order,
        }
