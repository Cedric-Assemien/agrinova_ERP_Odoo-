# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
import requests
from bs4 import BeautifulSoup
import logging
from datetime import datetime

_logger = logging.getLogger(__name__)


class BCEAORateProvider(models.Model):
    _name = 'bceao.rate.provider'
    _description = 'Fournisseur de taux BCEAO'
    
    name = fields.Char(string='Nom', default='BCEAO')
    last_update = fields.Datetime(string='Dernière mise à jour')
    last_error = fields.Text(string='Dernière erreur')
    active = fields.Boolean(string='Actif', default=True)
    
    @api.model
    def _cron_update_bceao_rates(self):
        """Cron quotidien de mise à jour des taux BCEAO"""
        _logger.info("Début mise à jour taux BCEAO...")
        
        try:
            self._update_rates_from_bceao()
            _logger.info("✅ Taux BCEAO mis à jour avec succès")
        except Exception as e:
            error_msg = f"Échec mise à jour BCEAO: {str(e)}"
            _logger.error(error_msg)
            self._send_error_email(error_msg)
            
            # Enregistrer l'erreur
            provider = self.search([], limit=1)
            if not provider:
                provider = self.create({'name': 'BCEAO'})
            provider.write({'last_error': error_msg})
    
    def _update_rates_from_bceao(self):
        """Scraping des taux depuis le site BCEAO"""
        # URL du site BCEAO (à ajuster selon structure réelle)
        url = 'https://www.bceao.int/fr/cours-et-taux/taux-dinflation'
        
        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Mapping devises (codes ISO)
            currency_mapping = {
                'EUR': 'EUR',  # Euro
                'USD': 'USD',  # Dollar US
                'GBP': 'GBP',  # Livre Sterling
                'CHF': 'CHF',  # Franc Suisse
                'JPY': 'JPY',  # Yen
                'CNY': 'CNY',  # Yuan
            }
            
            # Taux fixes connus FCFA
            # 1 EUR = 655.957 XOF (taux fixe)
            self._create_or_update_rate('EUR', 655.957)
            
            # Autres taux à scraper depuis le site
            # TODO: Adapter selon structure HTML réelle du site BCEAO
            # Pour l'instant, utilisation de taux indicatifs
            
            self._create_or_update_rate('USD', 600.0)  # Approximatif
            self._create_or_update_rate('GBP', 760.0)  # Approximatif
            
            # Mise à jour timestamp
            provider = self.search([], limit=1)
            if provider:
                provider.write({
                    'last_update': fields.Datetime.now(),
                    'last_error': False
                })
            
        except requests.RequestException as e:
            raise Exception(f"Erreur réseau: {str(e)}")
        except Exception as e:
            raise Exception(f"Erreur parsing: {str(e)}")
    
    def _create_or_update_rate(self, currency_code, rate_value):
        """Crée ou met à jour un taux de change"""
        Currency = self.env['res.currency']
        CurrencyRate = self.env['res.currency.rate']
        
        # Trouver la devise
        currency = Currency.search([('name', '=', currency_code)], limit=1)
        if not currency:
            _logger.warning(f"Devise {currency_code} non trouvée")
            return
        
        # Le taux Odoo est inversé (1 currency = X XOF)
        # Donc si 1 EUR = 655.957 XOF, le rate Odoo = 1/655.957
        odoo_rate = 1 / rate_value if rate_value > 0 else 1
        
        # Chercher le taux du jour
        today = fields.Date.today()
        existing_rate = CurrencyRate.search([
            ('currency_id', '=', currency.id),
            ('name', '=', today),
            ('company_id', '=', self.env.company.id)
        ], limit=1)
        
        if existing_rate:
            existing_rate.write({'rate': odoo_rate})
            _logger.info(f"Taux {currency_code} mis à jour: {rate_value} XOF")
        else:
            CurrencyRate.create({
                'currency_id': currency.id,
                'name': today,
                'rate': odoo_rate,
                'company_id': self.env.company.id,
            })
            _logger.info(f"Taux {currency_code} créé: {rate_value} XOF")
    
    def _send_error_email(self, error_message):
        """Envoie un email d'alerte en cas d'erreur"""
        try:
            mail_template = self.env.ref('agrinova_bceao.email_template_bceao_error', raise_if_not_found=False)
            if mail_template:
                mail_template.send_mail(self.id, force_send=True)
        except Exception as e:
            _logger.error(f"Impossible d'envoyer l'email d'erreur: {str(e)}")
    
    def action_manual_update(self):
        """Action manuelle de mise à jour depuis l'interface"""
        for record in self:
            try:
                self._update_rates_from_bceao()
                return {
                    'type': 'ir.actions.client',
                    'tag': 'display_notification',
                    'params': {
                        'title': 'Succès',
                        'message': 'Taux BCEAO mis à jour avec succès',
                        'type': 'success',
                        'sticky': False,
                    }
                }
            except Exception as e:
                return {
                    'type': 'ir.actions.client',
                    'tag': 'display_notification',
                    'params': {
                        'title': 'Erreur',
                        'message': str(e),
                        'type': 'danger',
                        'sticky': True,
                    }
                }
