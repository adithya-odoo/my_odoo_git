# -*- coding: utf-8 -*-

{
    'name': "Vehicle Management",
    'description': "Vehicle management",
    'application': True,
    'version': '17.0.1.0.0',

    'depends': [
         'base',
         'sale',
         'fleet',
         'hr',
         'mail',
         'account',
         'contacts',
         'base_automation',
    ],

    'data': [
        'data/load_data.xml',
        'data/labour_product.xml',
        'data/email_template.xml',
        'data/ir_cron_data.xml',
        'data/state_changing_automation_rule.xml',
        'report/ir_actions_report.xml',
        'report/vehicle_report.xml',
        'security/vehicle_management_security.xml',
        'security/ir.model.access.csv',
        'views/vehicle_management_views.xml',
        'views/customer.xml',
        'views/repair_tag_views.xml',
    ],

    'license': 'LGPL-3',
}
