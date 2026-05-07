"""
app_web.py : Serveur Flask pour le frontend web de ProPytho.
 
Fournit une API REST pour communiquer avec le système d'optimisation.
"""
 
from flask import Flask, render_template, request, jsonify
from models import Lait, Yaourt, Fromage, Ressource
from solver import ProblemeOptimisation, SimplexeSolver
import traceback
 
app = Flask(__name__, static_folder='static', template_folder='templates')
 
# Variables globales pour stocker l'état de l'application
current_problem = None
current_products = []
current_resources = []
 
 
@app.route('/')
def index():
    """Affiche la page principale."""
    return render_template('index.html')
 
 
@app.route('/api/default-data', methods=['GET'])
def get_default_data():
    """Retourne les données par défaut."""
    try:
        products_data = {
            'Lait': {
                'consommation_lait': 1.0,
                'profit_unitaire': 20,
                'description': 'Lait en sachet'
            },
            'Yaourt': {
                'consommation_lait': 1.2,
                'profit_unitaire': 40,
                'description': 'Yaourt'
            },
            'Fromage': {
                'consommation_lait': 8.0,
                'profit_unitaire': 300,
                'description': 'Fromage'
            }
        }
 
        resources_data = {
            'Lait cru': {
                'quantite': 1000,
                'unite': 'kg'
            },
            'Temps de travail': {
                'quantite': 160,
                'unite': 'heures'
            },
            'Capacite refrigeration': {
                'quantite': 500,
                'unite': 'kg'
            }
        }
 
        return jsonify({
            'success': True,
            'products': products_data,
            'resources': resources_data
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400
 
 
@app.route('/api/optimize', methods=['POST'])
def optimize():
    """Lance l'optimisation avec les donnees fournies."""
    try:
        data = request.get_json()
 
        # Valider les donnees
        if not data or 'products' not in data or 'resources' not in data:
            return jsonify({'success': False, 'error': 'Donnees manquantes'}), 400
 
        products_data = data['products']
        resources_data = data['resources']
 
        # Creer les produits avec les bons parametres
        produits = []
        if 'Lait' in products_data:
            # Pour le lait: cout_unitaire + profit_unitaire = prix_vente_unitaire
            cout_lait = 1.0  # Cout de base assume
            prix_lait = cout_lait + float(products_data['Lait']['profit_unitaire'])
            produits.append(Lait(cout_unitaire=cout_lait, prix_vente_unitaire=prix_lait))

        if 'Yaourt' in products_data:
            cout_yaourt = 2.0  # Cout de base assume
            prix_yaourt = cout_yaourt + float(products_data['Yaourt']['profit_unitaire'])
            produits.append(Yaourt(cout_unitaire=cout_yaourt, prix_vente_unitaire=prix_yaourt))

        if 'Fromage' in products_data:
            cout_fromage = 10.0  # Cout de base assume
            prix_fromage = cout_fromage + float(products_data['Fromage']['profit_unitaire'])
            produits.append(Fromage(cout_unitaire=cout_fromage, prix_vente_unitaire=prix_fromage))
 
        if not produits:
            return jsonify({'success': False, 'error': 'Aucun produit fourni'}), 400
 
        # Creer les ressources avec le bon mapping
        lait_dispo = float(resources_data.get('Lait cru', {}).get('quantite', 1000))
        heures_machine = float(resources_data.get('Capacite refrigeration', {}).get('quantite', 500))
        heures_mo = float(resources_data.get('Temps de travail', {}).get('quantite', 160))

        ressource = Ressource(
            lait_disponible=lait_dispo,
            heures_machine=heures_machine,
            heures_main_oeuvre=heures_mo
        )

        # Creer et resoudre le probleme
        problem = ProblemeOptimisation(produits=produits, ressources=ressource)
        solver = SimplexeSolver(problem)

        # resoudre() retourne (bool, Dict[str, float], float)
        success, solution, profit_total = solver.resoudre()

        # Stocker globalement pour references futures
        global current_problem, current_products, current_resources
        current_problem = problem
        current_products = produits
        current_resources = ressource

        # Preparer les resultats
        production = {}
        if success and solution:
            for product_name, quantity in solution.items():
                production[product_name] = quantity

        return jsonify({
            'success': success,
            'message': 'Optimisation reussie' if success else 'Echec de l\'optimisation',
            'production': production,
            'profit_total': profit_total if success else 0,
            'status': 'OPTIMAL' if success else 'INFEASIBLE',
            'iterations': 0  # PuLP ne retourne pas le nombre d'iterations
        })
        production = {}
        if succes:
            for produit in produits:
                quantite = solution.get(produit.nom, 0)
                production[produit.nom] = round(quantite, 4)
 
        return jsonify({
            'success': succes,
            'message': 'Solution optimale trouvée' if succes else 'Pas de solution optimale',
            'production': production,
            'profit_total': round(profit_optimal, 2) if succes else 0,
            'status': solver.statut or 'UNKNOWN',
            'iterations': 0  # PuLP ne retourne pas ce détail facilement
        })
 
    except Exception as e:
        import traceback
        print("ERROR in optimize API:")
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Erreur lors de l\'optimisation'
        }), 400
 
 
@app.route('/api/validate-inputs', methods=['POST'])
def validate_inputs():
    """Valide les donnees d'entree."""
    try:
        data = request.get_json()
        errors = {}
 
        if 'products' in data:
            for name, product in data['products'].items():
                try:
                    profit = float(product.get('profit_unitaire', 0))
                    consumption = float(product.get('consommation_lait', 0))
                    if profit < 0 or consumption <= 0:
                        errors[f'product_{name}'] = 'Valeurs invalides (profit >= 0, consommation > 0)'
                except ValueError:
                    errors[f'product_{name}'] = 'Valeurs doivent etre des nombres'
 
        if 'resources' in data:
            for name, resource in data['resources'].items():
                try:
                    quantity = float(resource.get('quantite', 0))
                    if quantity <= 0:
                        errors[f'resource_{name}'] = 'Quantite doit etre positive'
                except ValueError:
                    errors[f'resource_{name}'] = 'Quantite doit etre un nombre'
 
        return jsonify({
            'success': len(errors) == 0,
            'errors': errors
        })
 
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400
 
 
@app.route('/api/get-model', methods=['GET'])
def get_model():
    """Retourne le modele mathematique du probleme."""
    try:
        if not current_problem:
            return jsonify({'success': False, 'error': 'Aucun probleme charge'}), 400
 
        model_text = str(current_problem)
        return jsonify({'success': True, 'model': model_text})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400
 
 
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Resource not found'}), 404
 
 
@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500
 
 
if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=5000)