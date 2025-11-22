# -*- coding: utf-8 -*-
from odoo import models, fields


class ResCurrencyRate(models.Model):
    _inherit = 'res.currency.rate'
    
    source = fields.Selection(
        selection=[('manual', 'Manual'), ('bceao', 'BCEAO')],
        default='manual',
        string='Source',
        help='Source du taux de change'
    )
    
    def _name_get(self):
        result = []
        for rate in self:
            name = f"{rate.currency_id.name} - {rate.name}"
            if rate.source == 'bceao':
                name += " (BCEAO)"
            result.append((rate.id, name))
        return result
