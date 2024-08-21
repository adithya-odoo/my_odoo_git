# -*- coding: utf-8 -*-

{
    'name': "Vehicle Management",
    'description': "Vehicle management",
    'application': True,

    'depends': [
         'base',
        'sale',
         'fleet',
         'hr',
         'mail',
        'account',
        'contacts',
        'sale_management',
    ],

    'data': [
        'views/vehicle_management_views.xml',
        'views/customer.xml',
        'views/repair_tag_views.xml',
        'data/load_data.xml',
        'data/labour_product.xml',
        'data/email_template.xml',
        'data/ir_cron_data.xml',
        # 'data/automation_rule.xml',
        'security/vehicle_management_security.xml',
        'security/ir.model.access.csv',
    ]
}
