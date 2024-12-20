# -*- coding: utf-8 -*-
{
    'name': 'Fuel Control',
    'version': '3.0',
    'sequence': -1,
    'category': 'Inventory',
    'summary': 'Gestión del inventario de combustible',
    'description': 'Modulo para gestionar el inventario de combustible de la empresa.',
    'author': 'Luis Miguel GJ (LuisCodes)',
    'depends': ['base', 'web'],
    'data': [
        'views/fuel_control_views.xml',
        'security/ir.model.access.csv'

    ],
    'assets': {
        'web.assets_backend': [
            'fuel_control/static/src/components/*'
        ]
    },
    'installable': True,
    'application': True,
}