# -*- coding: utf-8 -*-
{
    'name': "mobile_money_management",

    'summary': "Gestion des dépôts, retraits et transferts d’argent mobile",

    'description': """
Ce module permet de gérer un point Mobile Money avec :
- Dépôts (Orange, Moov, MTN, Wave)
- Retraits (Orange, Moov, MTN, Wave)
- Transferts internationaux (Sénégal, Bénin, Burkina, Niger, Togo, Mali)
Avec détection automatique de l’opérateur et du pays selon le numéro de téléphone.
Vues disponibles : liste, formulaire, kanban, graphique et tableau croisé (pivot).
    """,

    'author': "Jun~~",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Services/Finance',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/depot_views.xml',
        'views/retrait_views.xml',
        'views/transfert_views.xml',
        'views/menus.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}

