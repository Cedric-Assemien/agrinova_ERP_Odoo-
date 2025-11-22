# AGRINOVA - Module Odoo pour AGRINOVA SARL

## Description

Module principal de gestion intégrée pour AGRINOVA SARL, entreprise ivoirienne spécialisée dans la transformation agroalimentaire (jus, confitures, farines locales).

## Fonctionnalités

- **Configuration centralisée** pour tous les paramètres métier
- **Groupes de sécurité** par département (Production, Qualité, Commercial, RH, etc.)
- **Navigation personnalisée** adaptée aux processus AGRINOVA
- **API REST** pour intégrations externes
- **Portail client** pour suivi des commandes

## Architecture

Ce module sert de hub central et dépend de:

### Modules Odoo Standard
- `sale_management` - Gestion des ventes
- `stock` - Gestion des stocks
- `mrp` - Production/Manufacturing
- `account` - Comptabilité
- `hr_payroll` - Paie
- `crm` - CRM
- `quality_control` - Contrôle qualité

### Modules AGRINOVA Complémentaires
- `agrinova_mobile_money` - Paiements Orange Money / MTN MoMo
- `agrinova_payroll_ci` - Paie Côte d'Ivoire (CNPS/ITS)
- `agrinova_bceao` - Taux de change BCEAO automatiques
- `agrinova_quality_alert` - Alertes qualité et péremption
- `agrinova_whatsapp` - Notifications WhatsApp automatisées
- `agrinova_dashboard` - Tableaux de bord métier
- `agrinova_production` - Extensions production et rendement

## Installation

```bash
# Dans le répertoire extra-addons
cd /path/to/odoo/extra-addons

# Redémarrer Odoo
odoo-bin -c odoo.conf -u agrinova

# Ou via l'interface
# Apps > Mettre à jour la liste des applications
# Rechercher "AGRINOVA" > Installer
```

## Configuration

Après installation:

1. Aller dans **AGRINOVA > Configuration > Paramètres**
2. Configurer les paramètres selon vos besoins:
   - Production (seuils, emplacements)
   - Qualité (contrôles, alertes péremption)
   - Commercial (conditions paiement, portail)
   - Paie (taux CNPS, ITS)
   - Notifications (Email, WhatsApp)
   - Taux BCEAO

## Utilisation

### Groupes de sécurité

- **Administrateur**: Accès complet + configuration
- **Responsable**: Gestion et supervision
- **Utilisateur**: Accès basique

groupes métier spécialisés:
- Équipe Commerciale
- Équipe Production
- Équipe Logistique
- Équipe Qualité
- Équipe Comptabilité
- Équipe RH

### API REST

```python
# Health check
GET /agrinova/api/health

# Configuration
POST /agrinova/api/config
```

## Structure

```
agrinova/
├── __init__.py
├── __manifest__.py
├── hooks.py
├── models/
│   ├── agrinova_config.py
│   └── res_config_settings.py
├── controllers/
│   └── main.py
├── views/
│   ├── agrinova_menu.xml
│   ├── agrinova_config_views.xml
│   └── res_config_settings_views.xml
├── security/
│   ├── agrinova_security.xml
│   └── ir.model.access.csv
├── data/
│   └── agrinova_data.xml
├── demo/
│   └── agrinova_demo.xml
├── reports/
│   └── agrinova_reports.xml
└── static/
    ├── description/
    │   ├── icon.png
    │   └── banner.png
    └── src/
        ├── css/
        │   ├── agrinova.css
        │   └── agrinova_portal.css
        └── js/
            └── agrinova.js
```

## Support

- **Version Odoo**: 18.0 Enterprise
- **Licence**: LGPL-3
- **Auteur**: AGRINOVA SARL
- **Site Web**: https://www.agrinova.ci

## Changelog

### Version 18.0.1.0.0 (2025-01)
- Version initiale
- Configuration centralisée
- Groupes de sécurité
- Navigation personnalisée
- API REST de base
