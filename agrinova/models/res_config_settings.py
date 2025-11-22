# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _


class ResConfigSettings(models.TransientModel):
    """Extension des paramètres de configuration pour AGRINOVA"""
    
    _inherit = 'res.config.settings'
    
    # Référence à la configuration AGRINOVA
    agrinova_config_id = fields.Many2one(
        'agrinova.config',
        string='Configuration AGRINOVA',
        compute='_compute_agrinova_config',
        store=False
    )
    
    # === PARAMETRES GENERAUX ===
    agrinova_fiscal_year_start = fields.Date(
        string='Début exercice fiscal',
        related='agrinova_config_id.fiscal_year_start',
        readonly=False
    )
    
    # === PARAMETRES PRODUCTION ===
    agrinova_default_production_location_id = fields.Many2one(
        'stock.location',
        string='Emplacement production',
        related='agrinova_config_id.default_production_location_id',
        readonly=False
    )
    
    agrinova_production_yield_warning_threshold = fields.Float(
        string='Seuil alerte rendement (%)',
        related='agrinova_config_id.production_yield_warning_threshold',
        readonly=False
    )
    
    # === PARAMETRES QUALITE ===
    agrinova_expiry_alert_days_before = fields.Integer(
        string='Alerte péremption (jours)',
        related='agrinova_config_id.expiry_alert_days_before',
        readonly=False
    )
    
    agrinova_quality_control_mandatory = fields.Boolean(
        string='Contrôle qualité obligatoire',
        related='agrinova_config_id.quality_control_mandatory',
        readonly=False
    )
    
    # === PARAMETRES COMMERCIAUX ===
    agrinova_default_payment_term_id = fields.Many2one(
        'account.payment.term',
        string='Conditions de paiement',
        related='agrinova_config_id.default_payment_term_id',
        readonly=False
    )
    
    agrinova_enable_customer_portal = fields.Boolean(
        string='Portail client',
        related='agrinova_config_id.enable_customer_portal',
        readonly=False
    )
    
    # === NOTIFICATIONS ===
    agrinova_enable_whatsapp_notifications = fields.Boolean(
        string='Notifications WhatsApp',
        related='agrinova_config_id.enable_whatsapp_notifications',
        readonly=False
    )
    
    agrinova_enable_email_notifications = fields.Boolean(
        string='Notifications Email',
        related='agrinova_config_id.enable_email_notifications',
        readonly=False
    )
    
    # === MOBILE MONEY ===
    agrinova_enable_mobile_money = fields.Boolean(
        string='Paiements Mobile Money',
        related='agrinova_config_id.enable_mobile_money',
        readonly=False
    )
    
    # === PAIE ===
    agrinova_payroll_cnps_rate_employee = fields.Float(
        string='Taux CNPS employé (%)',
        related='agrinova_config_id.payroll_cnps_rate_employee',
        readonly=False
    )
    
    agrinova_payroll_cnps_rate_employer = fields.Float(
        string='Taux CNPS employeur (%)',
        related='agrinova_config_id.payroll_cnps_rate_employer',
        readonly=False
    )
    
    agrinova_payroll_cnps_ceiling = fields.Float(
        string='Plafond CNPS (XOF)',
        related='agrinova_config_id.payroll_cnps_ceiling',
        readonly=False
    )
    
    # === TAUX BCEAO ===
    agrinova_auto_update_currency_rates = fields.Boolean(
        string='Mise à jour auto taux BCEAO',
        related='agrinova_config_id.auto_update_currency_rates',
        readonly=False
    )
    
    agrinova_bceao_update_time = fields.Char(
        string='Heure mise à jour BCEAO',
        related='agrinova_config_id.bceao_update_time',
        readonly=False
    )
    
    # === DASHBOARD ===
    agrinova_dashboard_refresh_interval = fields.Integer(
        string='Intervalle refresh dashboard (s)',
        related='agrinova_config_id.dashboard_refresh_interval',
        readonly=False
    )
    
    @api.depends('company_id')
    def _compute_agrinova_config(self):
        """Récupérer ou créer la configuration AGRINOVA pour la société"""
        AgrinovaConfig = self.env['agrinova.config']
        for record in self:
            config = AgrinovaConfig.search([
                ('company_id', '=', record.company_id.id),
                ('active', '=', True)
            ], limit=1)
            
            if not config:
                config = AgrinovaConfig.create({
                    'name': f'Configuration {record.company_id.name}',
                    'company_id': record.company_id.id,
                })
            
            record.agrinova_config_id = config
    
    def set_values(self):
        """Sauvegarder les valeurs de configuration"""
        res = super().set_values()
        # Les champs related sont automatiquement sauvegardés
        return res
    
    @api.model
    def get_values(self):
        """Récupérer les valeurs de configuration"""
        res = super().get_values()
        # Les champs related sont automatiquement chargés
        return res

    # === FIX: Champ manquant causant OwlError ===
    # Ce champ est utilisé par les vues Enterprise mais parfois manquant si le module
    # account_invoice_extract n'est pas installé correctement.
    # On le définit ici pour éviter le crash de l'interface.
    extract_in_invoice_digitalization_mode = fields.Selection(
        [('auto_send', 'Auto Send'), ('manual_send', 'Manual Send')],
        string='Digitization Mode',
        default='manual_send',
        store=False
    )

    extract_out_invoice_digitalization_mode = fields.Selection(
        [('auto_send', 'Auto Send'), ('manual_send', 'Manual Send')],
        string='Digitization Mode (Out)',
        default='manual_send',
        store=False
    )

    extract_single_line_per_tax = fields.Boolean(
        string='Single Line Per Tax',
        default=False,
        store=False
    )

    extract_can_show_send_button = fields.Boolean(
        string='Can Show Send Button',
        default=False,
        store=False
    )
