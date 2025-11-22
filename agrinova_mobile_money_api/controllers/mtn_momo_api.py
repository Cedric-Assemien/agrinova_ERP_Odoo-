# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
import logging

_logger = logging.getLogger(__name__)


class MTNMoMoAPI(http.Controller):
    
    @http.route('/mobile_money/mtn/webhook', type='json', auth='public', csrf=False)
    def mtn_momo_webhook(self, **kwargs):
        """Webhook pour notifications MTN MoMo"""
        _logger.info(f"MTN MoMo webhook received: {kwargs}")
        # TODO: Traiter callback MTN
        return {'status': 'success'}
    
    @http.route('/mobile_money/mtn/init', type='json', auth='user')
    def mtn_momo_init_payment(self, amount, phone_number):
        """Initier paiement MTN MoMo"""
        # TODO: Appel API MTN Collection
        _logger.info(f"Init MTN MoMo payment: {amount} XOF to {phone_number}")
        return {'status': 'pending', 'transaction_id': 'MTN123456'}
