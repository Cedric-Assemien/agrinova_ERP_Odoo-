# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class AgrinovaConfig(models.Model):
    """Configuration globale pour AGRINOVA"""
    
    _name = 'agrinova.config'
    _description = 'Configuration AGRINOVA'
    _order = 'company_id, id desc'
    
    name = fields.Char(
        string='Nom de configuration',
        required=True,
        default='Configuration AGRINOVA'
    )
    
    company_id = fields.Many2one(
        'res.company',
        string='Société',
        required=True,
        default=lambda self: self.env.company
    )
    
    active = fields.Boolean(
        string='Actif',
        default=True
    )
    
    # === PARAMETRES GENERAUX ===
    default_currency_id = fields.Many2one(
        'res.currency',
        string='Devise par défaut',
        default=lambda self: self.env.ref('base.XOF', raise_if_not_found=False),
        help='Franc CFA (XOF) pour Côte d\'Ivoire'
    )
    
    fiscal_year_start = fields.Date(
        string='Début exercice fiscal',
        default=fields.Date.today,
        help='Date de début de l\'exercice fiscal'
    )
    
    # === PARAMETRES PRODUCTION ===
    default_production_location_id = fields.Many2one(
        'stock.location',
        string='Emplacement production par défaut',
        domain="[('usage', '=', 'production')]"
    )
    
    production_yield_warning_threshold = fields.Float(
        string='Seuil d\'alerte rendement (%)',
        default=85.0,
        help='Alerter si le rendement de production est inférieur à ce seuil'
    )
    
    # === PARAMETRES QUALITE ===
    expiry_alert_days_before = fields.Integer(
        string='Alerte péremption (jours avant)',
        default=30,
        help='Nombre de jours avant péremption pour déclencher une alerte'
    )
    
    quality_control_mandatory = fields.Boolean(
        string='Contrôle qualité obligatoire',
        default=True,
        help='Rend le contrôle qualité obligatoire pour tous les produits finis'
    )
    
    # === PARAMETRES COMMERCIAUX ===
    default_payment_term_id = fields.Many2one(
        'account.payment.term',
        string='Conditions de paiement par défaut'
    )
    
    enable_customer_portal = fields.Boolean(
        string='Activer portail client',
        default=True,
        help='Permet aux clients d\'accéder à leurs commandes et factures en ligne'
    )
    
    # === NOTIFICATIONS ===
    enable_whatsapp_notifications = fields.Boolean(
        string='Notifications WhatsApp',
        default=False,
        help='Activer les notifications automatiques via WhatsApp'
    )
    
    enable_email_notifications = fields.Boolean(
        string='Notifications Email',
        default=True,
        help='Activer les notifications par email'
    )
    
    # === MOBILE MONEY ===
    enable_mobile_money = fields.Boolean(
        string='Paiements Mobile Money',
        default=False,
        help='Activer les paiements Orange Money et MTN MoMo'
    )
    
    # === PAIE ===
    payroll_cnps_rate_employee = fields.Float(
        string='Taux CNPS employé (%)',
        default=6.3,
        help='Taux de cotisation CNPS part employé (Côte d\'Ivoire)'
    )
    
    payroll_cnps_rate_employer = fields.Float(
        string='Taux CNPS employeur (%)',
        default=16.55,
        help='Taux de cotisation CNPS part employeur (Côte d\'Ivoire)'
    )
    
    payroll_cnps_ceiling = fields.Float(
        string='Plafond CNPS (XOF)',
        default=1647315.0,
        help='Plafond mensuel de cotisation CNPS'
    )
    
    # === TAUX BCEAO ===
    auto_update_currency_rates = fields.Boolean(
        string='Mise à jour automatique taux BCEAO',
        default=True,
        help='Importer automatiquement les taux de change BCEAO quotidiennement'
    )
    
    bceao_update_time = fields.Char(
        string='Heure mise à jour BCEAO',
        default='02:00',
        help='Heure d\'exécution du cron (format HH:MM)'
    )
    
    # === DASHBOARD ===
    dashboard_refresh_interval = fields.Integer(
        string='Intervalle rafraîchissement dashboard (secondes)',
        default=300,
        help='Intervalle de rafraîchissement automatique des données du dashboard'
    )
    
    # Métadonnées
    create_date = fields.Datetime(string='Date de création', readonly=True)
    write_date = fields.Datetime(string='Dernière modification', readonly=True)
    create_uid = fields.Many2one('res.users', string='Créé par', readonly=True)
    write_uid = fields.Many2one('res.users', string='Modifié par', readonly=True)
    
    @api.constrains('production_yield_warning_threshold')
    def _check_yield_threshold(self):
        """Valider le seuil de rendement"""
        for record in self:
            if record.production_yield_warning_threshold < 0 or record.production_yield_warning_threshold > 100:
                raise ValidationError(_('Le seuil de rendement doit être entre 0 et 100%'))
    
    @api.constrains('expiry_alert_days_before')
    def _check_expiry_alert_days(self):
        """Valider les jours d'alerte"""
        for record in self:
            if record.expiry_alert_days_before < 0:
                raise ValidationError(_('Le nombre de jours d\'alerte doit être positif'))
    
    @api.constrains('payroll_cnps_rate_employee', 'payroll_cnps_rate_employer')
    def _check_cnps_rates(self):
        """Valider les taux CNPS"""
        for record in self:
            if record.payroll_cnps_rate_employee < 0 or record.payroll_cnps_rate_employee > 100:
                raise ValidationError(_('Le taux CNPS employé doit être entre 0 et 100%'))
            if record.payroll_cnps_rate_employer < 0 or record.payroll_cnps_rate_employer > 100:
                raise ValidationError(_('Le taux CNPS employeur doit être entre 0 et 100%'))
    
    def get_config(self):
        """Récupérer la configuration active pour la société courante"""
        return self.search([
            ('company_id', '=', self.env.company.id),
            ('active', '=', True)
        ], limit=1)
    
    @api.model
    def create(self, vals):
        """Désactiver les autres configs lors de la création d'une nouvelle"""
        if vals.get('active'):
            self.search([
                ('company_id', '=', vals.get('company_id', self.env.company.id)),
                ('active', '=', True)
            ]).write({'active': False})
        return super().create(vals)
    
    def write(self, vals):
        """Désactiver les autres configs si celle-ci devient active"""
        if vals.get('active'):
            for record in self:
                self.search([
                    ('company_id', '=', record.company_id.id),
                    ('active', '=', True),
                    ('id', '!=', record.id)
                ]).write({'active': False})
        return super().write(vals)
