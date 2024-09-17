# -*- coding: utf-8 -*-

{
    'name': "Website Cart Remover",
    'description': "Website Cart Remover",
    'application': True,
    'version': '17.0.1.0.0',
    'license': 'LGPL-3',
    'depends': [
        'website_sale'
    ],

    'data':[
         'views/cart.xml'
    ],
'assets': {
    'web.assets_frontend': [
        'website_cart_remover/static/src/js/cart_remover.js',
        'website_cart_remover/static/src/css/cart_remover.css',

    ],
}
}