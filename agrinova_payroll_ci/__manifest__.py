# -*- coding: utf-8 -*-
{
    'name': 'AGRINOVA Paie Côte d\'Ivoire',
    'version': '18.0.1.0.0',
    'category': 'Human Resources/Payroll',
    'summary': 'Localisation de la paie pour la Côte d\'Ivoire (CNPS, ITS)',
    'description': """
        Paie Côte d'Ivoire - AGRINOVA
        ==============================
        
        Gestion complète de la paie selon la législation ivoirienne.
        
        Fonctionnalités:
        - Cotisations CNPS employé (6.3%) et employeur (16.55%)
        - Calcul ITS (Impôt sur Traitements et Salaires) avec barème progressif
        - Bulletins de paie conformes au format ivoirien
        - Exports CNPS et ITS pour déclarations
        - Plafonnement CNPS automatique (1,647,315 XOF)
        
        Réglementation 2024-2025
    """,
    'author': 'AGRINOVA SARL',
    'website': 'https://www.agrinova.ci',
    'license': 'LGPL-3',
    'depends': [
        'hr',
        'hr_payroll',
        'hr_contract',
    ],
    'data': [
        # Security
        'security/payroll_ci_security.xml',
        'security/ir.model.access.csv',
        
        # Data - Structures et règles
        'data/hr_payroll_structure_type_data.xml',
        'data/hr_payroll_structure_data.xml',
        'data/hr_salary_rule_category_data.xml',
        'data/hr_salary_rule_data.xml',
        
        # Views
        'views/hr_contract_views.xml',
        'views/hr_payslip_views.xml',
        
        # Wizards
        'wizard/export_cnps_wizard_views.xml',
        'wizard/export_its_wizard_views.xml',
        
        # Reports
        'reports/payslip_report.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
