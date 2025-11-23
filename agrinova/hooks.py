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
    
    # Configuration des comptes par défaut
    _setup_default_accounts(env)

def _setup_default_accounts(env):
    """Configure les comptes par défaut"""
    _logger.info('Setting up default accounts...')
    
    company = env.company
    
    # Récupérer les comptes créés par le fichier de données
    # Note: On utilise search car ref() n'est pas toujours dispo dans le hook sans xml_id complet
    acc_recv = env['account.account'].search([('code', '=', '411000'), ('company_id', '=', company.id)], limit=1)
    acc_pay = env['account.account'].search([('code', '=', '401000'), ('company_id', '=', company.id)], limit=1)
    acc_inc = env['account.account'].search([('code', '=', '701000'), ('company_id', '=', company.id)], limit=1)
    acc_exp = env['account.account'].search([('code', '=', '601000'), ('company_id', '=', company.id)], limit=1)
    
    if not all([acc_recv, acc_pay, acc_inc, acc_exp]):
        _logger.warning("Certains comptes par défaut n'ont pas été trouvés, configuration partielle.")
    
    # 1. Configurer les propriétés sur le partenaire (Client/Fournisseur)
    # On définit les valeurs par défaut pour le champ property_account_receivable_id/payable_id
    if acc_recv:
        _set_default_property(env, 'property_account_receivable_id', 'res.partner', acc_recv)
    if acc_pay:
        _set_default_property(env, 'property_account_payable_id', 'res.partner', acc_pay)
        
    # 2. Configurer les propriétés sur la catégorie de produit (Revenu/Dépense)
    if acc_inc:
        _set_default_property(env, 'property_account_income_categ_id', 'product.category', acc_inc)
    if acc_exp:
        _set_default_property(env, 'property_account_expense_categ_id', 'product.category', acc_exp)

def _set_default_property(env, field_name, model_name, value_record):
    """Helper pour définir une propriété par défaut"""
    try:
        Fields = env['ir.model.fields']
        field = Fields.search([('model', '=', model_name), ('name', '=', field_name)], limit=1)
        
        if not field:
            _logger.warning(f"Champ {field_name} non trouvé sur {model_name}")
            return

        Property = env['ir.property']
        # Vérifier si la propriété existe déjà pour la société (sans res_id = global default)
        prop = Property.search([
            ('name', '=', field_name),
            ('fields_id', '=', field.id),
            ('res_id', '=', False),
            ('company_id', '=', env.company.id)
        ], limit=1)
        
        value_ref = f"{value_record._name},{value_record.id}"
        
        if not prop:
            Property.create({
                'name': field_name,
                'fields_id': field.id,
                'value': value_ref,
                'company_id': env.company.id,
                'type': 'many2one',
            })
            _logger.info(f"Propriété {field_name} créée avec {value_record.name}")
        else:
            prop.write({'value': value_ref})
            _logger.info(f"Propriété {field_name} mise à jour")
            
    except Exception as e:
        _logger.error(f"Erreur lors de la configuration de {field_name}: {str(e)}")
