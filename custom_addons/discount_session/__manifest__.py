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
    ],

    'assets': {
        'point_of_sale._assets_pos': [
              'discount_session/static/src/xml/discount_session_pos.xml'
            ]
    }
}