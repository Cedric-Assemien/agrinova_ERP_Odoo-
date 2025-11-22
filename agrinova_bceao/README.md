# AGRINOVA Taux BCEAO

Module d'import automatique des taux de change BCEAO.

## Fonctionnalités

- Import quotidien automatique (02:00 UTC)
- Taux EUR/XOF fixe (655.957)
- Taux USD, GBP, etc. (à adapter selon site BCEAO)
- Mise à jour manuelle possible
- Alertes email en cas d'échec

## Installation

```bash
# Installer dépendances Python
pip install requests beautifulsoup4 lxml

# Activer le module
odoo-bin -u agrinova_bceao -d votre_database
```

## Configuration

Le cron s'exécute automatiquement chaque jour à 02:00 UTC.

Pour mise à jour manuelle:
1. Aller dans **Comptabilité > Configuration > Taux BCEAO**
2. Cliquer sur "Mise à Jour Manuelle"

## Notes Techniques

Le scraping doit être adapté selon la structure exacte du site BCEAO.
URL actuelle: https://www.bceao.int/

Taux fixes connus:
- 1 EUR = 655.957 XOF

## Support

AGRINOVA SARL - https://www.agrinova.ci
