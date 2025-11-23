# -*- coding: utf-8 -*-
from odoo import models, fields
from datetime import date
import requests
from bs4 import BeautifulSoup
import logging

_logger = logging.getLogger(__name__)

class ResCompany(models.Model):
    _inherit = 'res.company'

    currency_provider = fields.Selection([
        ('ecb', 'European Central Bank'),
        ('xe_com', 'xe.com'),
        ('cbuae', '[AE] Central Bank of the UAE'),
        ('bnb', '[BG] Bulgaria National Bank'),
        ('bbr', '[BR] Central Bank of Brazil'),
        ('boc', '[CA] Bank of Canada'),
        ('fta', '[CH] Federal Tax Administration of Switzerland'),
        ('mindicador', '[CL] Central Bank of Chile via mindicador.cl'),
        ('banrepco', '[CO] Bank of the Republic'),
        ('cnb', '[CZ] Czech National Bank'),
        ('cbegy', '[EG] Central Bank of Egypt'),
        ('banguat', '[GT] Bank of Guatemala'),
        ('mnb', '[HU] Magyar Nemzeti Bank'),
        ('bi', '[ID] Bank Indonesia'),
        ('boi', '[IT] Bank of Italy'),
        ('banxico', '[MX] Bank of Mexico'),
        ('bnm', '[MY] Bank Negara Malaysia'),
        ('bcrp', '[PE] SUNAT (replaces Bank of Peru)'),
        ('nbp', '[PL] National Bank of Poland'),
        ('bnr', '[RO] National Bank of Romania'),
        ('srb', '[SE] Sveriges Riksbank'),
        ('bsi', '[SI] Bank of Slovenia'),
        ('bot', '[TH] Bank of Thailand'),
        ('tcmb', '[TR] Central Bank of the Republic of Türkiye'),
        ('hmrc', '[UK] HM Revenue & Customs'),
        ('bcu', '[UY] Uruguayan Central Bank'),
        ('bceao', 'BCEAO'),
    ], string='Service', default='ecb')

    def _parse_bceao_data(self, available_currencies, *args, **kwargs):
        """
        Parse les données de la BCEAO pour mettre à jour les taux.
        Retourne un dictionnaire: {currency_code: (rate, date_str)}
        """
        print("DEBUG: _parse_bceao_data called!")
        
        # Vérification de la devise de base
        if self.currency_id.name != 'XOF':
            # Si la société n'est pas en XOF, on ne peut pas utiliser ce provider directement
            # sauf si on fait des conversions croisées. Pour l'instant, on suppose XOF.
            _logger.warning("BCEAO provider is designed for XOF base currency.")
        
        try:
            rates_dict = {}
            today_str = date.today().isoformat()
            
            url = 'https://www.bceao.int/fr/cours/cours-des-devises-contre-Franc-CFA-appliquer-aux-transferts'
            _logger.info(f"BCEAO: Fetching {url}")
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Trouver la table des devises
            # La structure peut varier, on cherche une table qui contient "Devise", "Achat", "Vente"
            table = soup.find('table')
            if not table:
                raise ValueError("Table des devises non trouvée sur la page BCEAO")

            # Mapping des noms de devises vers codes ISO
            currency_map = {
                'Euro': 'EUR',
                'Dollar us': 'USD',
                'Yen japonais': 'JPY',
                'Livre sterling': 'GBP',
                'Franc suisse': 'CHF',
                'Dollar canadien': 'CAD',
                'Yuan renminbi': 'CNY',
            }

            rows = table.find_all('tr')
            for row in rows:
                cols = row.find_all('td')
                if not cols:
                    continue
                
                currency_name = cols[0].get_text(strip=True)
                # Achat = cols[1], Vente = cols[2]
                # On utilise le taux de Vente (plus conservateur pour les dépenses) ou Achat ?
                # Le screenshot montre: Euro Achat=655.957 Vente=655.957
                # Dollar US Achat=564.750 Vente=571.750
                
                # Pour Odoo (1 unité étrangère = X XOF), on veut savoir combien de XOF pour 1 USD.
                # Si on achète du USD, la banque nous le vend à 571.750.
                # Donc 1 USD = 571.750 XOF.
                
                try:
                    # Nettoyage des valeurs (virgule -> point, espaces)
                    rate_str = cols[2].get_text(strip=True).replace(',', '.').replace(' ', '')
                    rate_value = float(rate_str)
                    
                    iso_code = currency_map.get(currency_name)
                    if not iso_code:
                        # Essayer de deviner ou logger
                        continue
                        
                    if iso_code in available_currencies:
                        # Odoo stocke le taux inverse: 1 XOF = (1/Rate) Devise
                        odoo_rate = 1.0 / rate_value
                        rates_dict[iso_code] = (odoo_rate, today_str)
                        _logger.info(f"BCEAO: Found {iso_code} = {rate_value} XOF -> Rate {odoo_rate}")
                        
                except (ValueError, IndexError) as e:
                    _logger.warning(f"BCEAO: Erreur parsing ligne {currency_name}: {e}")
                    continue

            # Fallback pour EUR si non trouvé (taux fixe)
            if 'EUR' in available_currencies and 'EUR' not in rates_dict:
                rates_dict['EUR'] = (1.0 / 655.957, today_str)

            _logger.info(f"BCEAO: Returning {len(rates_dict)} rates")
            return rates_dict
            
        except Exception as e:
            _logger.error(f"BCEAO: Erreur dans _parse_bceao_data: {str(e)}", exc_info=True)
            raise

