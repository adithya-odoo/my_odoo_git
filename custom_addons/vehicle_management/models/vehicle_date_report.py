# -*- coding: utf-8 -*-

from odoo import models, api


class VehicleDateReport(models.AbstractModel):
    _name = 'report.vehicle_management.report_vehicle_management'

    @api.model
    def _get_report_values(self, doc_ids, data=None):
        query = """ select name from vehicle_management where start_date between '%s' and '%s'"""% (data.get('start_date'),(data.get('end_date')))
        # query += """ and advisor_id = %d """% (data.get('advisor_ids'))
        print(query)
        self.env.cr.execute(query)
        report = self.env.cr.dictfetchall()
        print(report)
        # docs = self.env['vehicle.management'].browse(doc_ids)
        return {
            # 'doc_ids': doc_ids,
            'report': report,
            'doc_model': 'date.filter',
            # 'docs': docs,
            # 'data': data,
        }