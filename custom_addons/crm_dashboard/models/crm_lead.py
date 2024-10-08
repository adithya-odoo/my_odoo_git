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

        print(self.search_read([('company_id', '=', company_id.id),
                          ('user_id', '=', self.env.user.id)], ['activity_type_id',
                          'activity_ids']))
        print(self.search_read([('company_id', '=', company_id.id),
                          ('user_id', '=', self.env.user.id),
                                ('type', '=', 'lead')]))
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

    @api.model
    def get_pie_data(self):
        activities =  self.search([('company_id', '=', self.env.company.id),
                          ('user_id', '=', self.env.user.id)])
        activity_name = []
        activity_len = []
        for data in activities.activity_type_id:
            activity_len.append(len(activities.filtered(lambda r: r.activity_type_id.id == data.id)))
            activity_name.append(data.name)
        return {
             'name': activity_name,
             'data':activity_len
            }

    @api.model
    def get_bar_data(self):
        print("dugggd")
        company_id = self.env.company
        lost_leads = len(self.search([('company_id', '=', company_id.id),
                             ('user_id', '=', self.env.user.id),
                             ('type', '=', 'lead'),
                             ('active', '=',  False)]))
        lost_opportunity = len(self.search([('company_id', '=', company_id.id),
                                   ('user_id', '=', self.env.user.id),
                                   ('type', '=', 'opportunity'),
                                   ('active', '=',  False)]))
        print(lost_leads, "wihhdhh")
        print(lost_opportunity)
        return {
            'lost_leads':lost_leads,
            'lost_opportunity':lost_opportunity
        }

    @api.model
    def get_doughnut_data(self):
        medium = self.search([('company_id', '=', self.env.company.id),
                                  ('user_id', '=', self.env.user.id),
                                  ('type', '=', 'lead')])
        print(medium)
        medium_name = []
        medium_len = []
        for data in medium.medium_id:
            medium_len.append(len(medium.filtered(
                lambda r: r.medium_id.id == data.id)))
            medium_name.append(data.name)
        return {
            'name': medium_name,
            'data': medium_len
        }

    @api.model
    def get_line_data(self):
        campaign = self.search([('company_id', '=', self.env.company.id),
                                ('user_id', '=', self.env.user.id),
                                ('type', '=', 'lead')])
        print(campaign)
        campaign_name = []
        campaign_len = []
        for data in campaign.campaign_id:
            campaign_len.append(len(campaign.filtered(
                lambda r: r.campaign_id.id == data.id)))
            campaign_name.append(data.name)
        return {
            'name': campaign_name,
            'data': campaign_len
        }


