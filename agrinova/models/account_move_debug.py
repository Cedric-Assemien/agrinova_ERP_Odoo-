# -*- coding: utf-8 -*-
from odoo import models, api, fields, _
from odoo.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)


class AccountMoveDebug(models.Model):
    _inherit = 'account.move'
    
    # Fix for missing extract fields (document OCR/AI extraction feature)
    extract_error_message = fields.Text(string='Extract Error Message', readonly=True)
    extract_document_uuid = fields.Char(string='Extract Document UUID', readonly=True)
    extract_state = fields.Selection([
        ('no_extract_requested', 'No extract requested'),
        ('not_enough_credit', 'Not enough credit'),
        ('error_status', 'An error occurred'),
        ('waiting_extraction', 'Waiting extraction'),
        ('extract_not_ready', 'waiting extraction, but it is not ready'),
        ('waiting_validation', 'Waiting validation'),
        ('done', 'Completed flow')
    ], string='Extract State', default='no_extract_requested', readonly=True)
    extract_status_code = fields.Integer(string='Extract Status Code', readonly=True)
    extract_remote_id = fields.Integer(string='Extract Remote ID', readonly=True)
    extract_word_ids = fields.Many2many('account.move.line', string='Extract Words', readonly=True)
    extract_attachment_id = fields.Many2one('ir.attachment', string='Extract Attachment', readonly=True)
    extract_can_show_send_button = fields.Boolean(string='Can Show Send Button', default=False, readonly=True)
    extract_can_show_resend_button = fields.Boolean(string='Can Show Resend Button', default=False, readonly=True)
    extract_can_show_banners = fields.Boolean(string='Can Show Banners', default=False, readonly=True)

    def _post(self, soft=True):
        """Override to add detailed logging before posting"""
        _logger.info("=" * 80)
        _logger.info("TENTATIVE VALIDATION FACTURE - DEBUG AGRINOVA")
        _logger.info("=" * 80)
        for move in self:
            _logger.info(f"Facture: {move.name}")
            _logger.info(f"Partenaire: {move.partner_id.name}")
            _logger.info(f"Date facture: {move.invoice_date}")
            _logger.info(f"Date échéance facture: {move.invoice_date_due}")
            _logger.info(f"Conditions paiement: {move.invoice_payment_term_id.name if move.invoice_payment_term_id else 'AUCUNE !!!'}")
            _logger.info(f"Journal: {move.journal_id.name}")
            _logger.info("")
            _logger.info("LIGNES COMPTABLES:")
            for line in move.line_ids:
                _logger.info(f"  - Nom: {line.name}")
                _logger.info(f"    Compte: {line.account_id.code if line.account_id else 'NULL'} - {line.account_id.name if line.account_id else 'AUCUN'}")
                _logger.info(f"    Type compte: {line.account_id.account_type if line.account_id else 'N/A'}")
                _logger.info(f"    Date échéance ligne: {line.date_maturity if line.date_maturity else 'NULL !!!'}")
                _logger.info(f"    Débit: {line.debit}, Crédit: {line.credit}")
                _logger.info("")
        _logger.info("=" * 80)
        return super(AccountMoveDebug, self)._post(soft=soft)


class AccountMoveLineDebug(models.Model):
    _inherit = 'account.move.line'

    @api.model_create_multi
    def create(self, vals_list):
        """Override create to log line creation details"""
        for vals in vals_list:
            account_id = vals.get('account_id')
            if account_id:
                account = self.env['account.account'].browse(account_id)
                if account.account_type in ('asset_receivable', 'liability_payable'):
                    _logger.warning("=" * 80)
                    _logger.warning(f"CRÉATION LIGNE COMPTE DÉBITEUR/CRÉDITEUR")
                    _logger.warning(f"Compte: {account.code} - {account.name}")
                    _logger.warning(f"Type: {account.account_type}")
                    _logger.warning(f"date_maturity dans vals: {vals.get('date_maturity', 'ABSENT !!!')}")
                    _logger.warning(f"Autres champs: {vals.keys()}")
                    _logger.warning("=" * 80)
        
        return super(AccountMoveLineDebug, self).create(vals_list)

