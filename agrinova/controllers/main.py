# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import http
from odoo.http import request
import json


class AgrinovaController(http.Controller):
    """Contrôleur principal pour AGRINOVA"""
    
    @http.route('/agrinova/portal', type='http', auth='user', website=True)
    def agrinova_portal(self, **kwargs):
        """Portail AGRINOVA pour les utilisateurs"""
        values = {
            'company': request.env.company,
            'user': request.env.user,
        }
        return request.render('agrinova.portal_main', values)
    
    @http.route('/agrinova/api/health', type='json', auth='none', csrf=False)
    def api_health_check(self):
        """Health check endpoint pour intégrations"""
        return {
            'status': 'ok',
            'version': '18.0.1.0.0',
            'modules': {
                'agrinova': True,
                'agrinova_mobile_money': 'agrinova_mobile_money' in request.env.registry._init_modules,
                'agrinova_payroll_ci': 'agrinova_payroll_ci' in request.env.registry._init_modules,
                'agrinova_bceao': 'agrinova_bceao' in request.env.registry._init_modules,
                'agrinova_whatsapp': 'agrinova_whatsapp' in request.env.registry._init_modules,
            }
        }
    
    @http.route('/agrinova/api/config', type='json', auth='user')
    def api_get_config(self):
        """Récupérer la configuration AGRINOVA via API"""
        config = request.env['agrinova.config'].sudo().get_config()
        if not config:
            return {'error': 'Configuration not found'}
        
        return {
            'name': config.name,
            'company': config.company_id.name,
            'production_yield_threshold': config.production_yield_warning_threshold,
            'expiry_alert_days': config.expiry_alert_days_before,
            'mobile_money_enabled': config.enable_mobile_money,
            'whatsapp_enabled': config.enable_whatsapp_notifications,
        }
