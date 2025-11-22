# -*- coding: utf-8 -*-
from odoo import models, fields, api


class HrContract(models.Model):
    _inherit = 'hr.contract'
    
    # Champs spécifiques Côte d'Ivoire
    cnps_number = fields.Char(
        string='Numéro CNPS',
        help='Numéro d\'immatriculation CNPS de l\'employé'
    )
    
    its_exempt = fields.Boolean(
        string='Exonéré ITS',
        default=False,
        help='Cocher si le contrat bénéficie d\'une exonération ITS'
    )
    
    transport_allowance = fields.Monetary(
        string='Indemnité de Transport',
        help='Montant mensuel de l\'indemnité de transport'
    )
    
    housing_allowance = fields.Monetary(
        string='Indemnité de Logement',
        help='Montant mensuel de l\'indemnité de logement'
    )
    
    family_allowance = fields.Monetary(
        string='Allocations Familiales',
        help='Prestations familiales versées'
    )
    
    @api.depends('wage', 'transport_allowance', 'housing_allowance')
    def _compute_cnps_base(self):
        """Calcul de la base CNPS (plafonné à 1,647,315 XOF)"""
        for contract in self:
            base = contract.wage + contract.transport_allowance + contract.housing_allowance
            contract.cnps_base = min(base, 1647315)  # Plafond CNPS 2024
    
    cnps_base = fields.Monetary(
        string='Base CNPS',
        compute='_compute_cnps_base',
        store=True,
        help='Base de calcul CNPS (salaire plafonné)'
    )
