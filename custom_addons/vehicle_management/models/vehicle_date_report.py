# -*- coding: utf-8 -*-

from odoo import api, models


class VehicleDateReport(models.AbstractModel):
    _name = 'report.vehicle_management.report_vehicle_management'

    @api.model
    def _get_report_values(self, doc_ids, data=None):
        query = """ select model.name as vehicle_name, partner.name as customer_name,
                     users.name as advisor, vm.vehicle_number as vehicle_number, cat.name as cat,
					 upper(vm.state) as state, upper(vm.service_type) as service_type , vm.total_cost as cost,
					 vm.estimated_amount as estimated_amount from vehicle_management as vm
                     inner join res_partner as partner on partner.id = vm.partner_id
                     inner join fleet_vehicle_model as model on  model.id = vm.vehicle_id
				     inner join fleet_vehicle_model_category as cat on cat.id = vm.vehicle_type_id
					 inner join res_partner as users on users.id =  (select partner_id from res_users where id = advisor_id)"""

        if data.get('start_date') and data.get('end_date'):
            query += """ where start_date between '%s' and '%s' """% (data.get('start_date'), (data.get('end_date')))
        if data.get('customer_ids'):
            query += """ and partner_id in %s """% (str(tuple(data.get('customer_ids')))).replace(",)",")")
        if data.get('advisor_ids'):
            query += """ and advisor_id in %s """% (str(tuple(data.get('advisor_ids')))).replace(",)",")")

        print(query)

        self.env.cr.execute(query)
        report = self.env.cr.dictfetchall()
        print(report)
        print(data.get('advisor_len'))
        print(data.get('customer_len'))

        if data.get('advisor_ids'):
            for record in report:
                record['advisor_len'] = data.get('advisor_len')
        if data.get('customer_ids'):
            for record in report:
                record['customer_len'] = data.get('customer_len')
        print(report)
        docs = self.env['vehicle.management'].browse(doc_ids)
        return {
            'report': report,
            'doc_model': 'date.filter',
        }