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
        'views/vehicle_management_views.xml',
        'views/customer.xml',
        'views/repair_tag_views.xml',
        'data/load_data.xml',
        'data/labour_product.xml',
        'data/email_template.xml',
        'data/ir_cron_data.xml',
        'data/state_changing_automation_rule.xml',
        'security/vehicle_management_security.xml',
        'security/ir.model.access.csv',
    ],

    'license': 'LGPL-3',
}
