# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
import logging

_logger = logging.getLogger(__name__)


class OrangeMoneyAPI(http.Controller):
    
    @http.route('/mobile_money/orange/webhook', type='json', auth='public', csrf=False)
    def orange_money_webhook(self, **kwargs):
        """Webhook pour notifications Orange Money"""
        _logger.info(f"Orange Money webhook received: {kwargs}")
        # TODO: Traiter callback Orange Money
        return {'status': 'success'}
    
    @http.route('/mobile_money/orange/init', type='json', auth='user')
    def orange_money_init_payment(self, amount, phone_number):
        """Initier paiement Orange Money"""
        # TODO: Appel API Orange Money
        _logger.info(f"Init Orange Money payment: {amount} XOF to {phone_number}")
        return {'status': 'pending', 'transaction_id': 'OM123456'}
