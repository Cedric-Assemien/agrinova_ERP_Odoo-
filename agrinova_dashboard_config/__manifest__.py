# -*- coding: utf-8 -*-
{
    'name': 'AGRINOVA Dashboard Config',
    'version': '18.0.1.0.0',
    'category': 'Reporting',
    'summary': 'Dashboards préconfigurés pour AGRINOVA',
    'depends': ['spreadsheet_dashboard', 'spreadsheet_dashboard_sale', 'spreadsheet_dashboard_stock_account', 'spreadsheet_dashboard_mrp_account'],
    'data': [
        'security/ir.model.access.csv',
        'data/dashboards.xml',
    ],
    'installable': True,
}
