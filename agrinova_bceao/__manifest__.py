# -*- coding: utf-8 -*-
{
    'name': 'AGRINOVA Taux BCEAO',
    'version': '18.0.1.0.0',
    'category': 'Accounting/Localizations',
    'summary': 'Import automatique des taux de change BCEAO',
    'description': """
        Taux de Change BCEAO - AGRINOVA
        ================================
        
        Import automatique quotidien des taux de change officiels de la
        Banque Centrale des États de l'Afrique de l'Ouest (BCEAO).
        
        Fonctionnalités:
        - Cron quotidien à 02:00 UTC
        - Scraping du site BCEAO
        - Mise à jour automatique des taux XOF
        - Gestion d'erreurs avec retry
        - Alertes email en cas d'échec
        - Interface fallback manuel
    """,
    'author': 'AGRINOVA SARL',
    'website': 'https://www.agrinova.ci',
    'license': 'LGPL-3',
    'depends': [
        'account',
        'account_accountant',
    ],
    'external_dependencies': {
        'python': ['requests', 'beautifulsoup4', 'lxml'],
    },
    'data': [
        'security/ir.model.access.csv',
        'data/ir_cron.xml',
        'views/res_currency_rate_views.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
