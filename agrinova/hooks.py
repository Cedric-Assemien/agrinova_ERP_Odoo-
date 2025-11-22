# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import logging

_logger = logging.getLogger(__name__)


def post_init_hook(env):
    """Hook exécuté après l'installation du module"""
    _logger.info('=== AGRINOVA Module Installation ===')
    
    # Créer la configuration par défaut si elle n'existe pas
    AgrinovaConfig = env['agrinova.config']
    existing_config = AgrinovaConfig.search([
        ('company_id', '=', env.company.id),
        ('active', '=', True)
    ], limit=1)
    
    if not existing_config:
        _logger.info('Creating default AGRINOVA configuration...')
        AgrinovaConfig.create({
            'name': f'Configuration {env.company.name}',
            'company_id': env.company.id,
        })
        _logger.info('Default configuration created successfully')
    else:
        _logger.info('Configuration already exists, skipping creation')
    
    _logger.info('=== AGRINOVA Module Installed Successfully ===')
