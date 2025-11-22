# -*- coding: utf-8 -*-
{
    'name': 'AGRINOVA Quality Alert', 
    'version': '18.0.1.0.0',
    'category': 'Inventory/Quality',
    'summary': 'Alertes qualité et gestion péremption',
    'description': """Alertes automatiques pour produits proche de péremption avec notifications email et WhatsApp""",
    'author': 'AGRINOVA SARL',
    'website': 'https://www.agrinova.ci',
    'license': 'LGPL-3',
    'depends': ['quality_control', 'product_expiry', 'stock'],
    'data': [
        'security/ir.model.access.csv',
        'data/ir_cron.xml',
        'data/email_templates.xml',
        'views/stock_lot_views.xml',
    ],
    'installable': True,
    'application': False,
}
