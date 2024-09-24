{
    'name': "Pos Remover",
    'description': "Sample Module",
    'version': '17.0.1.0.0',
    'license': 'LGPL-3',
    'depends': [
        'base',
        'point_of_sale',
],

    'assets': {
        'point_of_sale._assets_pos': [
              'pos_remover/static/src/xml/single_remove_btn.xml',
              'pos_remover/static/src/js/single_remove_btn.js',
              'pos_remover/static/src/xml/remove_all_btn.xml',
              'pos_remover/static/src/js/remove_all_btn.js',
        ]
    },
}