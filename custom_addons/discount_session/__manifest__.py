# -*- coding: utf-8 -*-

{
    'name': "Discount Limit",
    'description': "Discount limit in pos",
    'version': '17.0.1.0.0',
    'license': 'LGPL-3',
    'depends': [
        'base',
        'point_of_sale',

    ],
    'data':[
        'views/discount_setting.xml',
        'views/pos_order_views.xml',
    ],

    'assets': {
        'point_of_sale._assets_pos': [
              'discount_session/static/src/js/discount_session.js',

            ]
    },
}