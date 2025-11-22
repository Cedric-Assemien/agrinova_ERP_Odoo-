# -*- coding: utf-8 -*-
{
    'name': 'AGRINOVA WhatsApp Config',
    'version': '18.0.1.0.0',
    'category': 'Marketing',
    'summary': 'Templates WhatsApp pour AGRINOVA',
    'depends': ['whatsapp', 'whatsapp_sale', 'whatsapp_delivery'],
    'data': [
        'security/ir.model.access.csv',
        'data/whatsapp_templates.xml',
    ],
    'installable': True,
}
