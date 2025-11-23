# -*- coding: utf-8 -*-
{
    'name': 'AGRINOVA - Gestion Intégrée',
    'version': '18.0.1.0.0',
    'category': 'Industries',
    'summary': 'Module de gestion intégrée pour AGRINOVA SARL - Production agroalimentaire',
    'description': """
        Module principal de gestion intégrée pour AGRINOVA SARL
        =========================================================
        
        Entreprise ivoirienne de transformation agroalimentaire (jus, confitures, farines locales).
        
        **Architecture Révisée (Audit 2025-11-21)**:
        - Réutilise les modules existants (mobile_money_management, whatsapp, spreadsheet_dashboard)
        - Étend avec des fonctionnalités spécifiques AGRINOVA
        - 6 modules AGRINOVA créés: Paie CI, BCEAO, Quality, WhatsApp, Mobile Money, Dashboard
        
        **Fonctionnalités principales**:
        - Configuration centralisée des paramètres métier
        - Groupes de sécurité par département
        - Navigation personnalisée pour processus AGRINOVA
        - API REST pour intégrations externes
    """,
    'author': 'AGRINOVA SARL',
    'website': 'https://www.agrinova.ci',
    'license': 'LGPL-3',
    'depends': [
        # === CORE ODOO ===
        'base',
        'web',
        
        # === MODULES STANDARD ===
        'sale_management',
        'crm',
        'stock',
        'product',
        'product_expiry',
        'mrp',
        'mrp_account',
        'account',
        # 'account_accountant',  # Enterprise module - commented out to avoid missing field errors
        'account_payment',
        'hr',
        'hr_payroll',
        'hr_contract',
        'quality_control',
        
        # === MODULES EXISTANTS (Extra-Addons) - TEMPORAIREMENT DÉSACTIVÉS ===
        # TODO: Corriger les erreurs XML dans mobile_money_management avant de réactiver
        # 'mobile_money_management',      # Dépôts/Retraits/Transferts Mobile Money
        'whatsapp',                     # Base WhatsApp
        'whatsapp_sale',                # WhatsApp pour ventes
        'whatsapp_delivery',            # WhatsApp pour livraisons
        'spreadsheet_dashboard',        # Dashboards
        'spreadsheet_dashboard_sale',   # Dashboard ventes
        'spreadsheet_dashboard_stock_account',  # Dashboard stock
        'spreadsheet_dashboard_mrp_account',    # Dashboard production
        
        # === MODULES AGRINOVA SPÉCIFIQUES (OPTIONNELS) ===
        # Ces modules sont maintenant optionnels et indépendants
        # Installez-les séparément selon vos besoins:
        # - agrinova_payroll_ci: Paie Côte d'Ivoire (CNPS/ITS)
        # - agrinova_bceao: Taux de change BCEAO
        # - agrinova_quality_alert: Alertes péremption
        # - agrinova_whatsapp_config: Templates WhatsApp
        # - agrinova_mobile_money_api: API Orange/MTN
        # - agrinova_dashboard_config: Dashboards préconfigurés
    ],
    'data': [
        # Security
        'security/agrinova_security.xml',
        'security/ir.model.access.csv',
        
        # Data
        'data/agrinova_data.xml',
        'data/account_journal_data.xml',
        'data/account_chart_data.xml',
        'data/account_payment_term_data.xml',
        
        # Views - IMPORTANT: Load action definitions before menus that reference them
        'views/agrinova_config_views.xml',
        'views/res_config_settings_views.xml',  # Contains action_agrinova_settings
        'views/agrinova_menu.xml',  # References action_agrinova_settings
        
        # Reports
        'reports/agrinova_reports.xml',
    ],
    'demo': [
        'demo/agrinova_demo.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'agrinova/static/src/css/agrinova.css',
            'agrinova/static/src/js/agrinova.js',
        ],
        'web.assets_frontend': [
            'agrinova/static/src/css/agrinova_portal.css',
        ],
    },
    'images': [
        'static/description/icon.png',
        'static/description/banner.png',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'currency': 'XOF',
    'price': 0.00,
    'post_init_hook': 'post_init_hook',
}
