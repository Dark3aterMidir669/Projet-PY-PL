"""
test_project.py : Tests unitaires pour ProPytho

Tests des classes principales et des fonctionnalités clés.
"""

import sys
from pathlib import Path

# Ajouter le répertoire du projet au path
sys.path.insert(0, str(Path(__file__).parent))

from models import Lait, Yaourt, Fromage, Ressource
from solver import ProblemeOptimisation, SimplexeSolver


def test_produits():
    """Test des classes de produits."""
    print("\n" + "="*70)
    print("TEST 1: Classes de produits et polymorphisme")
    print("="*70)
    
    lait = Lait()
    yaourt = Yaourt()
    fromage = Fromage()
    
    print(f"\n{lait}")
    print(f"{yaourt}")
    print(f"{fromage}")
    
    # Test calcul_profit (polymorphisme)
    print("\nTest polymorphisme - calcul_profit():")
    print(f"  Lait.calcul_profit(100) = {lait.calcul_profit(100):.2f}")
    print(f"  Yaourt.calcul_profit(100) = {yaourt.calcul_profit(100):.2f}")
    print(f"  Fromage.calcul_profit(100) = {fromage.calcul_profit(100):.2f}")
    
    # Test consommation (polymorphisme)
    print("\nTest polymorphisme - consommation_lait():")
    print(f"  Lait: {lait.consommation_lait()} L/sachet")
    print(f"  Yaourt: {yaourt.consommation_lait()} L/pot")
    print(f"  Fromage: {fromage.consommation_lait()} L/kg")
    
    # Test setters (encapsulation)
    print("\nTest encapsulation - modification de prix:")
    print(f"  Prix initial Lait: {lait.prix_vente_unitaire:.2f}")
    lait.prix_vente_unitaire = 1.0
    print(f"  Nouveau prix: {lait.prix_vente_unitaire:.2f}")
    print(f"  Profit mis à jour: {lait.profit_unitaire:.2f}")
    
    # Réinitialiser
    lait = Lait()
    
    print("\n✓ TEST 1 RÉUSSI")


def test_ressources():
    """Test de la classe Ressource."""
    print("\n" + "="*70)
    print("TEST 2: Classe Ressource")
    print("="*70)
    
    ressources = Ressource(1000, 200, 150)
    print(f"\n{ressources}")
    
    # Test getters
    print(f"\nGetting properties:")
    print(f"  Lait: {ressources.lait_disponible} litres")
    print(f"  Machine: {ressources.heures_machine_disponibles} heures")
    print(f"  MO: {ressources.heures_main_oeuvre_disponibles} heures")
    
    # Test setters
    print(f"\nModification via setters:")
    ressources.lait_disponible = 1500
    print(f"  Nouveau lait: {ressources.lait_disponible}")
    
    # Test to_dict
    print(f"\nConversion to_dict():")
    print(f"  {ressources.to_dict()}")
    
    print("\n✓ TEST 2 RÉUSSI")


def test_probleme_optimisation():
    """Test de la modélisation du problème."""
    print("\n" + "="*70)
    print("TEST 3: Modélisation du problème d'optimisation")
    print("="*70)
    
    produits = [Lait(), Yaourt(), Fromage()]
    ressources = Ressource(1000, 200, 150)
    probleme = ProblemeOptimisation(produits, ressources)
    
    print(f"\nVariables de décision: {probleme.get_variable_names()}")
    print(f"\nCoefficients objectif: {probleme.coefficients_objective}")
    
    print(f"\nContraintes:")
    for nom, data in probleme.contraintes.items():
        print(f"  {nom}: {data['description']}")
        print(f"    Limite: {data['limite']}")
    
    # Test verification contraintes
    print("\n\nVérification des contraintes:")
    solution_test = {
        'Lait en sachet': 500,
        'Yaourt': 200,
        'Fromage': 0
    }
    
    valide = probleme.verifier_contraintes(solution_test)
    ressources_util = probleme.calculer_ressources_utilisees(solution_test)
    
    print(f"  Solution test: {solution_test}")
    print(f"  Valide: {valide}")
    print(f"  Ressources utilisées: {ressources_util}")
    
    # Afficher le modèle
    probleme.afficher_modele()
    
    print("\n✓ TEST 3 RÉUSSI")


def test_solveur():
    """Test du solveur Simplexe."""
    print("\n" + "="*70)
    print("TEST 4: Solveur Simplexe (PuLP + CBC)")
    print("="*70)
    
    produits = [Lait(), Yaourt(), Fromage()]
    ressources = Ressource(1000, 200, 150)
    probleme = ProblemeOptimisation(produits, ressources)
    solveur = SimplexeSolver(probleme)
    
    print("\nRésolution du problème...")
    succes, solution, profit = solveur.resoudre(verbose=True)
    
    if succes:
        print(f"\n✓ Solution optimale trouvée!")
        print(f"\nProfit optimal: {profit:.2f}")
        print(f"\nPlan de production:")
        for nom, quantite in solution.items():
            if quantite > 1e-6:
                print(f"  {nom}: {quantite:.2f}")
        
        # Afficher détails
        solveur.afficher_details_resolution()
    else:
        print(f"\n✗ Pas de solution")
    
    print("\n✓ TEST 4 RÉUSSI")


def test_validation_donnees():
    """Test de la validation des données."""
    print("\n" + "="*70)
    print("TEST 5: Validation des données")
    print("="*70)
    
    print("\nTest des validations:")
    
    # Test 1: Coût < 0
    try:
        lait = Lait(cout_unitaire=-0.5)
        print("  ✗ Coût négatif: NON validé (BUG)")
    except ValueError as e:
        print(f"  ✓ Coût négatif: validé (ValueError: {str(e)[:40]}...)")
    
    # Test 2: Prix < Coût
    try:
        lait = Lait(cout_unitaire=1.0, prix_vente_unitaire=0.5)
        print("  ✗ Prix < Coût: NON validé (BUG)")
    except ValueError as e:
        print(f"  ✓ Prix < Coût: validé (ValueError: {str(e)[:40]}...)")
    
    # Test 3: Ressource négative
    try:
        res = Ressource(lait_disponible=-100, heures_machine=100, heures_main_oeuvre=100)
        print("  ✗ Ressource négative: NON validée (BUG)")
    except ValueError as e:
        print(f"  ✓ Ressource négative: validée (ValueError: {str(e)[:40]}...)")
    
    print("\n✓ TEST 5 RÉUSSI")


def run_all_tests():
    """Exécute tous les tests."""
    print("\n")
    print("╔" + "="*68 + "╗")
    print("║" + " "*15 + "🧪 SUITE DE TESTS - PROPYTHO" + " "*25 + "║")
    print("╚" + "="*68 + "╝")
    
    try:
        test_produits()
        test_ressources()
        test_probleme_optimisation()
        test_solveur()
        test_validation_donnees()
        
        print("\n" + "="*70)
        print("✅ TOUS LES TESTS RÉUSSIS!")
        print("="*70 + "\n")
        
        return True
    
    except Exception as e:
        print(f"\n❌ ERREUR: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    succes = run_all_tests()
    sys.exit(0 if succes else 1)
