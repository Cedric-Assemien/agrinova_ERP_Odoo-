# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError
import requests
import logging

_logger = logging.getLogger(__name__)


class MobileDepot(models.Model):
    _inherit = 'mobile.depot'
    
    api_transaction_id = fields.Char(string='ID Transaction API')
    api_status = fields.Selection([
        ('pending', 'En attente'),
        ('success', 'Succès'),
        ('failed', 'Échoué'),
    ], string='Statut API')
    
    payment_id = fields.Many2one('account.payment', string='Paiement Lié')
    
    def action_process_orange_money(self):
        """Traiter via API Orange Money"""
        # TODO: Implémenter appel API Orange Money
        # Nécessite credentials API
        _logger.info(f"Processing Orange Money deposit: {self.reference}")
        self.api_status = 'success'
        return True
    
    def action_process_mtn_momo(self):
        """Traiter via API MTN MoMo"""
        # TODO: Implémenter appel API MTN
        _logger.info(f"Processing MTN MoMo deposit: {self.reference}")
        self.api_status = 'success'
        return True
    
    def action_create_payment(self):
        """Créer paiement Odoo depuis dépôt mobile money"""
        if not self.payment_id:
            journal = self.env['account.journal'].search([('type', 'in', ('bank', 'cash'))], limit=1)
            if not journal:
                raise UserError(_("Aucun journal de type 'Banque' ou 'Espèces' n'a été trouvé. Veuillez en configurer un dans la comptabilité."))

            payment = self.env['account.payment'].create({
                'payment_type': 'inbound',
                'partner_type': 'customer',
                'amount': self.montant,
                'date': self.date_operation,
                'memo': f"Mobile Money - {self.reference}",
                'journal_id': journal.id,
            })
            self.payment_id = payment.id
        return self.payment_id
