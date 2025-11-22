# -*- coding: utf-8 -*-
{
    'name': 'AGRINOVA Mobile Money API',
    'version': '18.0.1.0.0',
    'category': 'Accounting/Payment',
    'summary': 'Intégration API Orange Money & MTN MoMo',
    'depends': [
        'mobile_money_management',
        'account',
        'account_payment',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/mobile_money_views.xml',
    ],
    'installable': True,
}
