from odoo import models, fields

class EstateLocataire(models.Model):
    _inherit = "res.partner"
    _description = 'Estate Locataire'

    est_locataire = fields.Boolean(string="Est un locataire")
