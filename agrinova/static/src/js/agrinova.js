/** @odoo-module **/

import { registry } from "@web/core/registry";
import { rpc } from "@web/core/network/rpc";

// AGRINOVA JavaScript Module

console.log("AGRINOVA Module loaded");

// Fonction utilitaire pour formater les montants en XOF
export function formatXOF(amount) {
    return new Intl.NumberFormat('fr-CI', {
        style: 'currency',
        currency: 'XOF',
        minimumFractionDigits: 0
    }).format(amount);
}

// Fonction utilitaire pour formater les pourcentages
export function formatPercent(value) {
    return `${value.toFixed(2)}%`;
}

// Service AGRINOVA
export const agrinovaService = {
    dependencies: [],
    async start(env) {
        return {
            /**
             * Récupérer la configuration AGRINOVA
             */
            async getConfig() {
                return await rpc('/agrinova/api/config');
            },

            /**
             * Vérifier le statut de santé
             */
            async healthCheck() {
                return await rpc('/agrinova/api/health');
            },

            /**
             * Formater un montant
             */
            formatAmount(amount) {
                return formatXOF(amount);
            },

            /**
             * Formater un pourcentage
             */
            formatPercent(value) {
                return formatPercent(value);
            }
        };
    },
};

registry.category("services").add("agrinova", agrinovaService);
