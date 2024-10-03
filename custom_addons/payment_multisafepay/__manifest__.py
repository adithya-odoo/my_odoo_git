# -*- coding: utf-8 -*-

{
    'name': 'Payment Provider: Multisafe Pay',
    'version': '17.0.1.0.0',
    'category': 'Accounting/Payment Providers',
    'depends': ['payment',
                'base'],
    'data': [
            'views/payment_provider_view.xml',
            'views/payment_provider_template.xml',
            'data/payment_provider_data.xml',
            'data/account_payment_method.xml',
    ],
    'installable': True,
    'license': 'LGPL-3'
}
