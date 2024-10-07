# -*- coding: utf-8 -*-
{
    'name': 'Fuel Control',
    'version': '1.0',
    'category': 'Inventory',
    'summary': 'Gestión del inventario de combustible',
    'description': 'Modulo para gestionar el inventario de combustible de la empresa.',
    'author': 'Luis Miguel GJ (LuisCodes)',
    'depends': ['base', 'web'],
    'data': [
        'views/fuel_control_views.xml',
        'views/fuel_onboarding_panel.xml',
        'security/ir.model.access.csv'

    ],
    'installable': True,
    'application': True,
}