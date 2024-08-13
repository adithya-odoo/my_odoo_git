# -*- coding: utf-8 -*-

{
    'name': "Vehicle Management",
    'description': "Vehicle management",
    'application': True,

    'depends': [
         'base',
         'fleet',
         'hr',
         'mail',

    ],

    'data': [
        'views/vehicle_management_views.xml',
        'views/repair_tag_views.xml',
        'data/load_data.xml',
        'security/ir.model.access.csv',
    ]
}
