# -*- coding: utf-8 -*-

{
    'name' : 'Tolerance',
    'version': '17.0.1.0.0',

    'depends': [
        'base',
        'purchase',
        'sale_management',
        'stock',
    ],

    'data': [
        'security/ir.model.access.csv',
        'views/res_partner.xml',
        'views/warning_wizard.xml',
        'views/sale_order_line.xml',
        'views/purchase_order.xml',
    ],

    'license': 'LGPL-3',
}