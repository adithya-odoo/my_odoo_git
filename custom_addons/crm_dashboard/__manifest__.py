# -*- coding: utf-8 -*-

{
    'name': "Crm Dashboard",
    'version': '1.0',
    'installable': True,
    'depends': ['base',
                'crm'],
    'data':[
        'views/crm_dashboard_menu.xml',
    ],
    'assets': {
        'web.assets_backend': [
                 'crm_dashboard/static/src/js/crm_dashboard.js',
                 'crm_dashboard/static/src/xml/crm_dashboard.xml',
        ]
    }

}