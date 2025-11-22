from odoo import models, fields, api
from odoo.exceptions import ValidationError


class TransfertInternational(models.Model):
    _name = "mobile.transfert"
    _description = "Transfert International"

    reference = fields.Char(string="Référence", required=True, copy=False, default="Nouveau")
    expediteur = fields.Char(string="Nom de l'expéditeur", required=True)
    destinataire = fields.Char(string="Nom du destinataire", required=True)
    numero_international = fields.Char(string="Numéro international", required=True)

    pays = fields.Selection([
        ('sn', 'Sénégal (+221)'),
        ('bj', 'Bénin (+229)'),
        ('bf', 'Burkina Faso (+226)'),
        ('ne', 'Niger (+227)'),
        ('tg', 'Togo (+228)'),
        ('ml', 'Mali (+223)'),
    ], string="Pays", compute="_compute_pays_operateur", store=True)

    operateur = fields.Selection([
        ('orange', 'Orange'),
        ('moov', 'Moov'),
        ('mtn', 'MTN'),
    ], string="Opérateur", compute="_compute_pays_operateur", store=True)

    montant = fields.Float(string="Montant", required=True)
    date_operation = fields.Datetime(string="Date de l'opération", default=fields.Datetime.now)

    @api.depends('numero_international')
    def _compute_pays_operateur(self):
        """
        Détection automatique du pays via l'indicatif international
        et de l'opérateur via le préfixe local.
        """
        codes = {
            '+221': 'sn',  # Sénégal
            '+229': 'bj',  # Bénin
            '+226': 'bf',  # Burkina Faso
            '+227': 'ne',  # Niger
            '+228': 'tg',  # Togo
            '+223': 'ml',  # Mali
        }

        for rec in self:
            rec.pays = False
            rec.operateur = False

            if rec.numero_international:
                # Nettoyage du numéro (suppression espaces et tirets)
                numero_clean = rec.numero_international.replace(' ', '').replace('-', '')

                # Vérification avec indicatifs complets
                for indicatif, code_pays in codes.items():
                    if numero_clean.startswith(indicatif):
                        rec.pays = code_pays
                        numero_local = numero_clean[len(indicatif):]

                        # Détection de l'opérateur selon le préfixe local
                        if numero_local.startswith('01') or numero_local.startswith('91'):  # Moov variants
                            rec.operateur = 'moov'
                        elif numero_local.startswith('07') or numero_local.startswith('77'):  # Orange variants
                            rec.operateur = 'orange'
                        elif numero_local.startswith('04') or numero_local.startswith('64'):  # MTN variants
                            rec.operateur = 'mtn'
                        break

                # Fallback : vérification sans le signe +
                if not rec.pays and numero_clean.startswith('00'):
                    numero_clean = '+' + numero_clean[2:]  # 00221 -> +221
                    for indicatif, code_pays in codes.items():
                        if numero_clean.startswith(indicatif):
                            rec.pays = code_pays
                            numero_local = numero_clean[len(indicatif):]

                            if numero_local.startswith('01') or numero_local.startswith('91'):
                                rec.operateur = 'moov'
                            elif numero_local.startswith('07') or numero_local.startswith('77'):
                                rec.operateur = 'orange'
                            elif numero_local.startswith('04') or numero_local.startswith('64'):
                                rec.operateur = 'mtn'
                            break

    @api.constrains('pays', 'operateur')
    def _check_pays_operateur(self):
        """
        Bloque la sauvegarde si le pays ou l'opérateur n'a pas été détecté.
        """
        for rec in self:
            if not rec.pays:
                raise ValidationError(
                    "Impossible de détecter le pays. Vérifiez l'indicatif du numéro international (+221, +223, +226, +227, +228, +229).")
            if not rec.operateur:
                raise ValidationError(
                    "Impossible de détecter l'opérateur. Vérifiez le préfixe du numéro (Orange=07/77, Moov=01/91, MTN=04/64).")

    @api.constrains('numero_international')
    def _check_numero_international_format(self):
        """
        Validation du format du numéro international
        """
        for rec in self:
            if rec.numero_international:
                # Nettoyage du numéro
                numero_clean = rec.numero_international.replace(' ', '').replace('-', '')

                # Vérification de la présence d'un indicatif pays valide
                indicatifs_valides = ['+221', '+223', '+226', '+227', '+228', '+229']
                indicatif_trouve = False
                numero_local = ""

                for indicatif in indicatifs_valides:
                    if numero_clean.startswith(indicatif):
                        indicatif_trouve = True
                        numero_local = numero_clean[len(indicatif):]
                        break

                # Fallback pour format 00xxx
                if not indicatif_trouve and numero_clean.startswith('00'):
                    numero_temp = '+' + numero_clean[2:]
                    for indicatif in indicatifs_valides:
                        if numero_temp.startswith(indicatif):
                            indicatif_trouve = True
                            numero_local = numero_temp[len(indicatif):]
                            break

                if not indicatif_trouve:
                    raise ValidationError(
                        "Le numéro doit commencer par un indicatif pays valide : +221, +223, +226, +227, +228, +229.")

                # Vérification de la partie locale (10 chiffres)
                if len(numero_local) != 10:
                    raise ValidationError("La partie locale du numéro doit contenir exactement 10 chiffres.")

                if not numero_local.isdigit():
                    raise ValidationError("La partie locale du numéro ne doit contenir que des chiffres.")

                # Vérification du préfixe local
                prefixes_valides = ['01', '04', '07', '77', '91', '64']
                if not any(numero_local.startswith(prefix) for prefix in prefixes_valides):
                    raise ValidationError(
                        "Le numéro local doit commencer par un préfixe valide : 01/91 (Moov), 04/64 (MTN), 07/77 (Orange).")

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
        """
        Génération automatique de la référence en fonction de l'opérateur.
        """
        records = super().create(vals_list)

        prefix_map = {
            'orange': 'TRF/OM/',
            'moov': 'TRF/MV/',
            'mtn': 'TRF/MN/',
        }

        for record in records:
            if record.operateur and record.reference == "Nouveau":
                prefix = prefix_map.get(record.operateur, 'TRF/XX/')

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