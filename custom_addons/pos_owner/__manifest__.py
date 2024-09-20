# -*- coding: utf-8 -*-

{
    'name': "Product Owner",
    'description': "Product owner in pos",
    'version': '17.0.1.0.0',
    'license': 'LGPL-3',
    'depends': [
        'base',
        'point_of_sale',
        'sale_management',

    ],
    'data':[
        'views/product_owner.xml',
    ],

    'assets': {
        'point_of_sale._assets_pos': [
            'pos_owner/static/src/js/pos_props.js',
            'pos_owner/static/src/xml/pos_owner.xml',
            'pos_owner/static/src/xml/props.xml',
            'pos_owner/static/src/xml/pos_orderline.xml',
        ]
    },
}