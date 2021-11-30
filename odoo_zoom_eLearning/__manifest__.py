# -*- coding: utf-8 -*-
{
    "name": "Zoom - E-Learning Connector ",
    "summary": "Integrates Zoom with eLearning Platform",
    "description": """App which integrate Zoom with odoo eLearning to arrange Zoom online events. 
    It also integrate Odoo eLearning module with events for Multi User""",
    'author': "Syncoria Inc.",
    'website': "https://www.syncoria.com",
    'company': 'Syncoria Inc.',
    'maintainer': 'Syncoria Inc.',
    "category": "Extra Tools",
    "version": "13.0.1.0.0",
    "depends": ["base_eLearningevent_online"],
    "images": [
            'static/description/banner.png',
        ],
    "data": [
        "views/inherit_res_user_ZOOM.xml",
        'views/res_config_settings_views.xml',


    ],
    'support': "support@syncoria.com",
    'price': 100,
    'currency': 'USD',
    'license': 'OPL-1',
    'support': "support@syncoria.com",
    'installable': True,
    'application': False,
    'auto_install': False,
}
