// ProPytho Web Application - Main JavaScript

class ProPythoApp {
    constructor() {
        this.currentData = null;
        this.currentResults = null;
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.loadDefaultData();
    }

    setupEventListeners() {
        // Tab switching
        document.querySelectorAll('.tab-button').forEach(button => {
            button.addEventListener('click', () => this.switchTab(button.dataset.tab));
        });

        // Button events
        document.getElementById('load-default-btn').addEventListener('click', () => this.loadDefaultData());
        document.getElementById('optimize-btn').addEventListener('click', () => this.runOptimization());
        document.getElementById('validate-btn').addEventListener('click', () => this.validateInputs());
    }

    switchTab(tabName) {
        // Hide all tabs
        document.querySelectorAll('.tab-content').forEach(tab => tab.classList.remove('active'));
        document.querySelectorAll('.tab-button').forEach(btn => btn.classList.remove('active'));

        // Show selected tab
        document.getElementById(tabName).classList.add('active');
        event.target.classList.add('active');
    }

    async loadDefaultData() {
        try {
            this.showMessage('Chargement des donnees par defaut...', 'info');

            const response = await fetch('/api/default-data');
            const result = await response.json();

            if (result.success) {
                this.fillFormData(result.products, result.resources);
                this.showMessage('Donnees par defaut chargees avec succes', 'success');
                this.currentData = { products: result.products, resources: result.resources };
            } else {
                this.showMessage('Erreur lors du chargement des donnees', 'error');
            }
        } catch (error) {
            this.showMessage('Erreur reseau: ' + error.message, 'error');
            console.error('Error loading default data:', error);
        }
    }

    fillFormData(products, resources) {
        // Fill product data
        if (products.Lait) {
            document.getElementById('lait-profit').value = products.Lait.profit_unitaire;
            document.getElementById('lait-consumption').value = products.Lait.consommation_lait;
        }
        if (products.Yaourt) {
            document.getElementById('yaourt-profit').value = products.Yaourt.profit_unitaire;
            document.getElementById('yaourt-consumption').value = products.Yaourt.consommation_lait;
        }
        if (products.Fromage) {
            document.getElementById('fromage-profit').value = products.Fromage.profit_unitaire;
            document.getElementById('fromage-consumption').value = products.Fromage.consommation_lait;
        }

        // Fill resource data
        if (resources['Lait cru']) {
            document.getElementById('resource-lait').value = resources['Lait cru'].quantite;
        }
        if (resources['Temps de travail']) {
            document.getElementById('resource-temps').value = resources['Temps de travail'].quantite;
        }
        if (resources['Capacite refrigeration']) {
            document.getElementById('resource-frigo').value = resources['Capacite refrigeration'].quantite;
        }
    }

    getFormData() {
        return {
            products: {
                Lait: {
                    profit_unitaire: parseFloat(document.getElementById('lait-profit').value),
                    consommation_lait: parseFloat(document.getElementById('lait-consumption').value),
                    description: 'Lait en sachet'
                },
                Yaourt: {
                    profit_unitaire: parseFloat(document.getElementById('yaourt-profit').value),
                    consommation_lait: parseFloat(document.getElementById('yaourt-consumption').value),
                    description: 'Yaourt'
                },
                Fromage: {
                    profit_unitaire: parseFloat(document.getElementById('fromage-profit').value),
                    consommation_lait: parseFloat(document.getElementById('fromage-consumption').value),
                    description: 'Fromage'
                }
            },
            resources: {
                'Lait cru': {
                    quantite: parseFloat(document.getElementById('resource-lait').value),
                    unite: 'kg'
                },
                'Temps de travail': {
                    quantite: parseFloat(document.getElementById('resource-temps').value),
                    unite: 'heures'
                },
                'Capacite refrigeration': {
                    quantite: parseFloat(document.getElementById('resource-frigo').value),
                    unite: 'kg'
                }
            }
        };
    }

    validateFormData(data) {
        const errors = [];

        // Validate products
        for (const [name, product] of Object.entries(data.products)) {
            if (isNaN(product.profit_unitaire) || product.profit_unitaire < 0) {
                errors.push(`${name}: Profit doit etre non negatif et numerique`);
            }
            if (isNaN(product.consommation_lait) || product.consommation_lait <= 0) {
                errors.push(`${name}: Consommation doit etre positive`);
            }
        }

        // Validate resources
        for (const [name, resource] of Object.entries(data.resources)) {
            if (isNaN(resource.quantite) || resource.quantite <= 0) {
                errors.push(`${name}: Quantite doit etre positive`);
            }
        }

        return errors;
    }

    async validateInputs() {
        try {
            const data = this.getFormData();
            const errors = this.validateFormData(data);

            if (errors.length > 0) {
                errors.forEach(error => this.showMessage(error, 'warning'));
            } else {
                this.showMessage('Toutes les donnees sont valides', 'success');
            }
        } catch (error) {
            this.showMessage('Erreur de validation: ' + error.message, 'error');
        }
    }

    async runOptimization() {
        try {
            const data = this.getFormData();
            const errors = this.validateFormData(data);

            if (errors.length > 0) {
                errors.forEach(error => this.showMessage(error, 'error'));
                return;
            }

            this.showMessage('Optimisation en cours...', 'info');
            this.disableOptimizeButton();

            const response = await fetch('/api/optimize', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            });

            const result = await response.json();

            if (result.success) {
                this.currentResults = result;
                this.displayResults(result);
                this.showMessage('Optimisation reussie', 'success');
                this.switchTab('results');
                this.loadModelData();
            } else {
                this.showMessage('Echec: ' + result.message, 'error');
            }
        } catch (error) {
            this.showMessage('Erreur reseau: ' + error.message, 'error');
            console.error('Error during optimization:', error);
        } finally {
            this.enableOptimizeButton();
        }
    }

    displayResults(results) {
        const resultsContent = document.getElementById('results-content');
        
        let html = '<div class="results-grid">';

        // Profit total
        html += `
            <div class="result-card">
                <h4>Profit Total</h4>
                <div class="result-value">${results.profit_total.toFixed(2)}</div>
                <div class="result-unit">Devises</div>
            </div>
        `;

        // Production quantities
        for (const [product, quantity] of Object.entries(results.production)) {
            html += `
                <div class="result-card">
                    <h4>${product}</h4>
                    <div class="result-value">${quantity.toFixed(2)}</div>
                    <div class="result-unit">unites</div>
                </div>
            `;
        }

        // Status
        const statusClass = results.success ? 'status-success' : 'status-error';
        html += `
            <div class="result-card">
                <h4>Statut</h4>
                <div class="status-badge ${statusClass}">
                    ${results.status || 'OPTIMAL'}
                </div>
                <div class="result-unit">Iterations: ${results.iterations || 0}</div>
            </div>
        `;

        html += '</div>';

        // Add detailed table
        html += this.getDetailedResultsTable(results);

        resultsContent.innerHTML = html;
    }

    getDetailedResultsTable(results) {
        let html = '<h3 style="margin-top: 30px;">Production Detaillee</h3>';
        html += '<table style="width:100%; border-collapse: collapse; margin-top: 15px;">';
        html += '<thead><tr style="background: #ecf0f1; border-bottom: 2px solid #bdc3c7;">';
        html += '<th style="padding: 10px; text-align: left; border: 1px solid #bdc3c7;">Produit</th>';
        html += '<th style="padding: 10px; text-align: right; border: 1px solid #bdc3c7;">Quantite</th>';
        html += '<th style="padding: 10px; text-align: right; border: 1px solid #bdc3c7;">Profit Unitaire</th>';
        html += '<th style="padding: 10px; text-align: right; border: 1px solid #bdc3c7;">Profit Total</th>';
        html += '</tr></thead><tbody>';

        for (const [product, quantity] of Object.entries(results.production)) {
            const profitUnit = this.getProfitForProduct(product);
            const profitTotal = quantity * profitUnit;
            html += `<tr style="border-bottom: 1px solid #ecf0f1;">`;
            html += `<td style="padding: 10px; border: 1px solid #bdc3c7;">${product}</td>`;
            html += `<td style="padding: 10px; text-align: right; border: 1px solid #bdc3c7;">${quantity.toFixed(2)}</td>`;
            html += `<td style="padding: 10px; text-align: right; border: 1px solid #bdc3c7;">${profitUnit.toFixed(2)}</td>`;
            html += `<td style="padding: 10px; text-align: right; border: 1px solid #bdc3c7;">${profitTotal.toFixed(2)}</td>`;
            html += `</tr>`;
        }

        html += '<tr style="background: #ecf0f1; font-weight: bold; border-top: 2px solid #bdc3c7;">';
        html += '<td style="padding: 10px; border: 1px solid #bdc3c7;">TOTAL</td>';
        html += '<td style="padding: 10px; text-align: right; border: 1px solid #bdc3c7;">-</td>';
        html += '<td style="padding: 10px; text-align: right; border: 1px solid #bdc3c7;">-</td>';
        html += `<td style="padding: 10px; text-align: right; border: 1px solid #bdc3c7;">${results.profit_total.toFixed(2)}</td>`;
        html += '</tr>';

        html += '</tbody></table>';
        return html;
    }

    getProfitForProduct(product) {
        const profitInputs = {
            'Lait': 'lait-profit',
            'Yaourt': 'yaourt-profit',
            'Fromage': 'fromage-profit'
        };
        const inputId = profitInputs[product];
        if (inputId) {
            return parseFloat(document.getElementById(inputId).value) || 0;
        }
        return 0;
    }

    async loadModelData() {
        try {
            const response = await fetch('/api/get-model');
            const result = await response.json();

            if (result.success) {
                const modelContent = document.getElementById('model-content');
                modelContent.innerHTML = `<pre class="model-code">${this.escapeHtml(result.model)}</pre>`;
            }
        } catch (error) {
            console.error('Error loading model:', error);
        }
    }

    showMessage(text, type = 'info') {
        const messagesContainer = document.getElementById('messages');
        const messageEl = document.createElement('div');
        messageEl.className = `message ${type}`;
        messageEl.innerHTML = `
            <span>${text}</span>
            <span class="message-close" onclick="this.parentElement.remove()">x</span>
        `;
        messagesContainer.appendChild(messageEl);

        // Auto-remove after 5 seconds
        setTimeout(() => {
            if (messageEl.parentElement) {
                messageEl.remove();
            }
        }, 5000);
    }

    disableOptimizeButton() {
        const btn = document.getElementById('optimize-btn');
        btn.disabled = true;
        btn.innerHTML = 'Optimisation en cours...';
    }

    enableOptimizeButton() {
        const btn = document.getElementById('optimize-btn');
        btn.disabled = false;
        btn.innerHTML = 'LANCER OPTIMISATION';
    }

    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
}

// Initialize app when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    window.app = new ProPythoApp();
});
