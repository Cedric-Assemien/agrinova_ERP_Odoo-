# AGRINOVA Paie Côte d'Ivoire

Module de localisation de la paie pour la Côte d'Ivoire.

## Fonctionnalités

### Cotisations CNPS
- **Employé**: 6.3% du salaire brut plafonné
- **Employeur**: 16.55% du salaire brut plafonné
- **Plafond 2024**: 1,647,315 XOF

### ITS (Impôt sur Traitements et Salaires)
- Barème progressif 2024
- 9 tranches d'imposition (0% à 35%)
- Calcul automatique sur net imposable

### Exports
- Export Excel CNPS (déclarations mensuelles)
- Export Excel ITS (déclarations fiscales)

## Installation

```bash
# Installer les dépendances
pip install openpyxl

# Activer le module dans Odoo
odoo-bin -u agrinova_payroll_ci -d votre_database
```

## Configuration

1. Aller dans **RH > Configuration > Entreprise**
2. Renseigner le numéro employeur CNPS
3. Vérifier les taux CNPS (par défaut correctement configurés)

## Utilisation

1. Créer un contrat avec les informations CI (numéro CNPS, indemnités)
2. Générer un bulletin de paie
3. Les calculs CNPS et ITS sont automatiques
4. Exporter via boutons "Export CNPS" ou "Export ITS"

## Support

AGRINOVA SARL - https://www.agrinova.ci
