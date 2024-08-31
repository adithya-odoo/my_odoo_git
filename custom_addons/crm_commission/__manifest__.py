# -*- coding: utf-8 -*-

{
    'name' : 'Crm Commission',
    'version': '17.0.1.0.0',

    'depends': [
        'base',
        'crm',
        'sale_management',
    ],

    'data': [
        'security/ir.model.access.csv',
        'views/crm_commission.xml',
        'views/crm_team.xml',
        'views/crm_salesperson.xml',
    ],

    'license': 'LGPL-3',
}