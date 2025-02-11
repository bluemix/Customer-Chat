# -*- coding: utf-8 -*-
{
    'name': 'Customer Chat',
    'version': '17.0.0.0.1',
    'category': 'Discuss',
    'summary': '''Basic Customer Chat for Odoo''',
    'description': '''A simple module for a chat that enables customers to send
messages to customer service.''',
    'author': 'Abdulmomen Bsruki',
    'maintainer': 'Abdulmomen Bsruki',
    'website': 'bluemix.me',
    'depends': ['base', 'mail', 'bus', 'web'],
    'data': [
        'security/ir.model.access.csv',
        'views/chat_page_template.xml',
        'views/customer_chat_session_views.xml',
    ],
    'assets': {
        "web.assets_frontend": [
            "customer_chat/static/src/xml/chat_widget.xml",
            "customer_chat/static/src/js/chat_widget.js",
            "customer_chat/static/src/scss/chat_widget.scss",
        ]
    },
    'license': 'AGPL-3',
    'installable': True,
    'auto_install': False,
    'application': True
}
