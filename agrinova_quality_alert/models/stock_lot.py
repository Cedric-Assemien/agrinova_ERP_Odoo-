# -*- coding: utf-8 -*-
from odoo import models, fields, api
from datetime import datetime, timedelta
import logging

_logger = logging.getLogger(__name__)


class StockLot(models.Model):
    _inherit = 'stock.lot'
    
    alert_status = fields.Selection([
        ('ok', 'OK'),
        ('warning', 'À Surveiller'),
        ('expiring', 'Expirant'),
        ('expired', 'Expiré'),
    ], string='Statut Alerte', compute='_compute_alert_status', store=True)
    
    days_to_expiry = fields.Integer(
        string='Jours avant péremption',
        compute='_compute_days_to_expiry',
        store=True
    )
    
    @api.depends('expiration_date')
    def _compute_days_to_expiry(self):
        for lot in self:
            if lot.expiration_date:
                # Convert datetime to date if needed
                expiry_date = lot.expiration_date
                if isinstance(expiry_date, datetime):
                    expiry_date = expiry_date.date()
                delta = expiry_date - fields.Date.today()
                lot.days_to_expiry = delta.days
            else:
                lot.days_to_expiry = 9999
    
    @api.depends('days_to_expiry')
    def _compute_alert_status(self):
        config = self.env['agrinova.config'].get_config()
        threshold = config.expiry_alert_days_before or 30
        
        for lot in self:
            if lot.days_to_expiry < 0:
                lot.alert_status = 'expired'
            elif lot.days_to_expiry <= threshold:
                lot.alert_status = 'expiring'
            elif lot.days_to_expiry <= threshold * 2:
                lot.alert_status = 'warning'
            else:
                lot.alert_status = 'ok'
    
    @api.model
    def _cron_send_expiry_alerts(self):
        """Cron quotidien d'envoi d'alertes péremption"""
        _logger.info("Envoi des alertes de péremption...")
        
        expiring_lots = self.search([
            ('alert_status', 'in', ['expiring', 'expired']),
            ('product_qty', '>', 0)
        ])
        
        if not expiring_lots:
            _logger.info("Aucun lot à alerter")
            return
        
        # Grouper par statut
        expired = expiring_lots.filtered(lambda l: l.alert_status == 'expired')
        expiring = expiring_lots.filtered(lambda l: l.alert_status == 'expiring')
        
        # Envoyer emails
        if expired:
            self._send_alert_email(expired, 'expired')
        if expiring:
            self._send_alert_email(expiring, 'expiring')
        
        _logger.info(f"✅ Alertes envoyées: {len(expired)} expirés, {len(expiring)} expirants")
    
    def _send_alert_email(self, lots, alert_type):
        """Envoie email d'alerte pour les lots"""
        template_id = 'agrinova_quality_alert.email_template_expiry_alert'
        template = self.env.ref(template_id, raise_if_not_found=False)
        
        if not template:
            _logger.warning(f"Template {template_id} non trouvé")
            return
        
        # Envoyer un email par lot
        for lot in lots:
            try:
                template.send_mail(lot.id, force_send=True)
            except Exception as e:
                _logger.error(f"Erreur envoi email lot {lot.name}: {str(e)}")
