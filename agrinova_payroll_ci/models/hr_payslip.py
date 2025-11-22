# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError


class HrPayslip(models.Model):
    _inherit = 'hr.payslip'
    
    cnps_employee = fields.Monetary(
        string='CNPS Employé',
        compute='_compute_cnps_its',
        store=True,
        help='Cotisation CNPS part employé (6.3%)'
    )
    
    cnps_employer = fields.Monetary(
        string='CNPS Employeur',
        compute='_compute_cnps_its',
        store=True,
        help='Cotisation CNPS part employeur (16.55%)'
    )
    
    its_amount = fields.Monetary(
        string='ITS',
        compute='_compute_cnps_its',
        store=True,
        help='Impôt sur Traitements et Salaires'
    )
    
    net_imposable = fields.Monetary(
        string='Net Imposable ITS',
        compute='_compute_cnps_its',
        store=True,
        help='Base de calcul ITS (après déduction CNPS employé)'
    )
    
    @api.depends('line_ids', 'line_ids.total')
    def _compute_cnps_its(self):
        """Calcul automatique CNPS et ITS"""
        for payslip in self:
            # Récupération du salaire brut
            brut_line = payslip.line_ids.filtered(lambda l: l.code == 'BRUT')
            salaire_brut = brut_line.total if brut_line else 0
            
            # Calcul CNPS (plafonné)
            base_cnps = min(salaire_brut, 1647315)  # Plafond 2024
            payslip.cnps_employee = base_cnps * 0.063
            payslip.cnps_employer = base_cnps * 0.1655
            
            # Calcul ITS (net imposable = brut - CNPS employé)
            payslip.net_imposable = salaire_brut - payslip.cnps_employee
            payslip.its_amount = payslip._calculate_its(payslip.net_imposable)
    
    def _calculate_its(self, net_imposable):
        """
        Calcul ITS selon barème progressif 2024
        Tranches ITS Côte d'Ivoire:
        - 0 à 50,000: 0%
        - 50,001 à 130,000: 1.5%
        - 130,001 à 200,000: 5%
        - 200,001 à 300,000:10%
        - 300,001 à 500,000: 15%
        - 500,001 à 1,000,000: 20%
        - 1,000,001 à 1,500,000: 25%
        - 1,500,001 à 3,000,000: 30%
        - Plus de 3,000,000: 35%
        """
        if net_imposable <= 50000:
            return 0
        
        its = 0
        tranches = [
            (50000, 0),
            (80000, 0.015),   # 130,000 - 50,000
            (70000, 0.05),    # 200,000 - 130,000
            (100000, 0.10),   # 300,000 - 200,000
            (200000, 0.15),   # 500,000 - 300,000
            (500000, 0.20),   # 1,000,000 - 500,000
            (500000, 0.25),   # 1,500,000 - 1,000,000
            (1500000, 0.30),  # 3,000,000 - 1,500,000
        ]
        
        reste = net_imposable
        
        for montant_tranche, taux in tranches:
            if reste <= montant_tranche:
                its += reste * taux
                break
            else:
                its += montant_tranche * taux
                reste -= montant_tranche
        
        # Dernier tranche (plus de 3,000,000)
        if reste > 0:
            its += reste * 0.35
        
        return round(its, 0)  # ITS arrondi
    
    def action_export_cnps(self):
        """Ouvre le wizard d'export CNPS"""
        return {
            'type': 'ir.actions.act_window',
            'name': 'Export CNPS',
            'res_model': 'export.cnps.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_payslip_ids': self.ids,
            }
        }
    
    def action_export_its(self):
        """Ouvre le wizard d'export ITS"""
        return {
            'type': 'ir.actions.act_window',
            'name': 'Export ITS',
            'res_model': 'export.its.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_payslip_ids': self.ids,
            }
        }
