# -*- coding: utf-8 -*-
from odoo import models, fields


class ResCompany(models.Model):
    _inherit = 'res.company'
    
    cnps_employer_number = fields.Char(
        string='Numéro Employeur CNPS',
        help='Numéro d\'affiliation de l\'entreprise à la CNPS'
    )
    
    cnps_rate_employee = fields.Float(
        string='Taux CNPS Employé (%)',
        default=6.3,
        help='Taux de cotisation CNPS part employé (défaut: 6.3%)'
    )
    
    cnps_rate_employer = fields.Float(
        string='Taux CNPS Employeur (%)',
        default=16.55,
        help='Taux de cotisation CNPS part employeur (défaut: 16.55%)'
    )
    
    cnps_ceiling = fields.Monetary(
        string='Plafond CNPS',
        default=1647315,
        help='Plafond mensuel de cotisation CNPS (XOF)'
    )
    
    its_enabled = fields.Boolean(
        string='Activer ITS',
        default=True,
        help='Activer le calcul automatique de l\'ITS'
    )
