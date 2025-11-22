# -*- coding: utf-8 -*-
from odoo import models, fields


class AccountPayment(models.Model):
    _inherit = 'account.payment'
    
    mobile_money_transaction_id = fields.Char(string='Ref Mobile Money')
    is_mobile_money = fields.Boolean(string='Paiement Mobile Money', default=False)
