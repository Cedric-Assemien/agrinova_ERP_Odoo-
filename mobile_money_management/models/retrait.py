from odoo import models, fields, api
from odoo.exceptions import ValidationError


class RetraitMobile(models.Model):
    _name = "mobile.retrait"
    _description = "Retrait Mobile Money"

    reference = fields.Char(string="Référence", required=True, copy=False, default="Nouveau")
    client = fields.Char(string="Nom du client", required=True)
    numero = fields.Char(string="Numéro de téléphone", required=True)

    operateur = fields.Selection([
        ('orange', 'Orange'),
        ('moov', 'Moov'),
        ('mtn', 'MTN'),
        ('wave', 'Wave'),
    ], string="Opérateur", compute="_compute_operateur", store=True)

    compte_wave = fields.Boolean(string="Compte Wave ?")
    montant = fields.Float(string="Montant", required=True)
    date_operation = fields.Datetime(string="Date de l'opération", default=fields.Datetime.now)

    @api.depends('numero', 'compte_wave')  # Ajout de 'compte_wave' dans les dépendances
    def _compute_operateur(self):
        """
        Détecte automatiquement l'opérateur en fonction du préfixe du numéro
        """
        for rec in self:
            rec.operateur = False
            if rec.compte_wave:
                rec.operateur = 'wave'
            elif rec.numero:
                # Nettoyage du numéro (suppression espaces et caractères spéciaux)
                numero_clean = rec.numero.replace(' ', '').replace('-', '').replace('+225', '')

                if numero_clean.startswith('01'):
                    rec.operateur = 'moov'
                elif numero_clean.startswith('07'):
                    rec.operateur = 'orange'
                elif numero_clean.startswith('04'):
                    rec.operateur = 'mtn'

    @api.constrains('operateur')
    def _check_operateur(self):
        """
        Bloque la sauvegarde si aucun opérateur n'est détecté
        """
        for rec in self:
            if not rec.operateur:
                raise ValidationError("Numéro invalide : aucun opérateur reconnu (Orange=07, Moov=01, MTN=05).")

    @api.constrains('numero')
    def _check_numero_format(self):
        """
        Validation du format du numéro de téléphone (10 chiffres, commence par 01, 05 ou 07)
        """
        for rec in self:
            if rec.numero:
                # Nettoyage du numéro
                numero_clean = rec.numero.replace(' ', '').replace('-', '').replace('+225', '')

                # Vérification de la longueur (10 chiffres)
                if len(numero_clean) != 10:
                    raise ValidationError("Le numéro de téléphone doit contenir exactement 10 chiffres.")

                # Vérification que ce sont bien des chiffres
                if not numero_clean.isdigit():
                    raise ValidationError("Le numéro de téléphone ne doit contenir que des chiffres.")

                # Vérification du préfixe
                if not (numero_clean.startswith('01') or numero_clean.startswith('04') or numero_clean.startswith(
                        '07')):
                    raise ValidationError("Le numéro doit commencer par 01 (Moov), 04 (MTN) ou 07 (Orange).")

    @api.constrains('montant')
    def _check_montant(self):
        """
        Validation du montant (doit être supérieur à 0)
        """
        for rec in self:
            if rec.montant <= 0:
                raise ValidationError("Le montant doit être supérieur à 0.")

    @api.model_create_multi  # Meilleure pratique pour Odoo 18
    def create(self, vals_list):
        """Génération automatique de la référence selon l'opérateur"""
        records = super().create(vals_list)

        prefix_map = {
            'orange': 'RET/OM/',
            'moov': 'RET/MV/',
            'mtn': 'RET/MN/',
            'wave': 'RET/WE/',
        }

        for record in records:
            if record.operateur and record.reference == "Nouveau":
                prefix = prefix_map.get(record.operateur, 'RET/XX/')

                # Recherche du dernier enregistrement pour cet opérateur
                domain = [
                    ('operateur', '=', record.operateur),
                    ('reference', '!=', 'Nouveau'),
                    ('reference', 'like', prefix)
                ]
                last = self.search(domain, order="id desc", limit=1)

                if last and last.reference:
                    try:
                        # Extraction du numéro après le préfixe
                        number_part = last.reference.replace(prefix, '')
                        number = int(number_part) + 1
                    except (ValueError, IndexError):
                        number = 1
                else:
                    number = 1

                record.reference = f"{prefix}{str(number).zfill(3)}"

        return records

    @api.onchange('compte_wave')
    def _onchange_compte_wave(self):
        """Recalcul de l'opérateur quand on change le statut Wave"""
        if self.compte_wave:
            self.operateur = 'wave'
        else:
            # Recalcul basé sur le numéro si Wave est décoché
            self._compute_operateur()