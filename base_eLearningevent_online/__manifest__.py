# -*- coding: utf-8 -*-
{
    'name': "base_eLearningevent_online",
    "summary": "Syncoria Odoo eLearning Events Integration Base",
    "description": """Syncoria Odoo eLearning Events Integration Base""",
    'author': "Syncoria Inc.",
    'website': "https://www.syncoria.com",
    'company': 'Syncoria Inc.',
    'license': 'OPL-1',
    'support': "support@syncoria.com",
    'maintainer': 'Syncoria Inc.',
    "category": "Extra Tools",
    "version": "14.0.0.0.0",
    "depends": ["base_event_online","website_slides"],
    'data': [
        'views/elearning_event_custom_form.xml',
        'views/inherit_slide_channel_view_form.xml',
        'views/website_slides_course_main_inherit.xml',
    ],
}
