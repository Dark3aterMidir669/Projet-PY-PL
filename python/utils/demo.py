"""
demo.py : Démonstration automatique du projet ProPytho

Ce script exécute automatiquement les étapes principales du projet
sans intervention de l'utilisateur, pour montrer le fonctionnement complet.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from models import Lait, Yaourt, Fromage, Ressource
from solver import ProblemeOptimisation, SimplexeSolver
from utils import afficher_banner, afficher_separation


def demo_complete():
    """Exécute une démonstration complète du projet."""
    
    afficher_banner()
    
    # ========== ÉTAPE 1 : Initialisation des produits ==========
    
    afficher_separation("=")
    print("\n📋 ÉTAPE 1 : INITIALISATION DES PRODUITS")
    print("="*70)
    
    print("\nCréation des 3 produits laitiers :")
    produits = [
        Lait(cout_unitaire=0.3, prix_vente_unitaire=0.8),
        Yaourt(cout_unitaire=0.6, prix_vente_unitaire=1.5),
        Fromage(cout_unitaire=1.5, prix_vente_unitaire=4.5)
    ]
    
    for i, produit in enumerate(produits, 1):
        print(f"\n{i}. {produit}")
    
    # ========== ÉTAPE 2 : Définition des ressources ==========
    
    afficher_separation("=")
    print("\n♻️  ÉTAPE 2 : DÉFINITION DES RESSOURCES")
    print("="*70)
    
    ressources = Ressource(
        lait_disponible=1000,
        heures_machine=200,
        heures_main_oeuvre=150
    )
    
    print("\n" + str(ressources))
    
    # ========== ÉTAPE 3 : Modélisation du problème ==========
    
    afficher_separation("=")
    print("\n⚙️  ÉTAPE 3 : MODÉLISATION DU PROBLÈME")
    print("="*70)
    
    probleme = ProblemeOptimisation(produits, ressources)
    
    print("\n📊 Variables de décision (x_i = quantité du produit i):")
    for i, nom in enumerate(probleme.get_variable_names(), 1):
        print(f"   x_{i} = {nom}")
    
    print("\n📈 Fonction objectif (coefficients de profit):")
    for nom, coeff in probleme.coefficients_objective.items():
        print(f"   {coeff:.4f} * {nom}")
    
    print("\n📐 Contraintes:")
    for nom, data in probleme.contraintes.items():
        print(f"   • {data['description']}")
    
    # Afficher le modèle complet
    probleme.afficher_modele()
    
    # ========== ÉTAPE 4 : Résolution par le Simplexe ==========
    
    afficher_separation("=")
    print("\n🔧 ÉTAPE 4 : RÉSOLUTION PAR LE SIMPLEXE")
    print("="*70)
    
    solveur = SimplexeSolver(probleme)
    
    print("\n[SOLVEUR] Construction du problème PuLP...")
    print("[SOLVEUR] Utilisation de PuLP + CBC (COIN-OR)")
    print("[SOLVEUR] Implémentation : Algorithme du Simplexe")
    
    succes, solution, profit = solveur.resoudre(verbose=True)
    
    # ========== ÉTAPE 5 : Analyse des résultats ==========
    
    if succes:
        afficher_separation("=")
        print("\n✅ ÉTAPE 5 : ANALYSE DES RÉSULTATS")
        print("="*70)
        
        print("\n🎯 SOLUTION OPTIMALE TROUVÉE!")
        print("-" * 70)
        
        # Plan de production
        print("\n📊 Plan de production optimal :")
        for produit in produits:
            quantite = solution.get(produit.nom, 0)
            if quantite > 1e-6:
                profit_prod = produit.calcul_profit(quantite)
                pct_profit = (profit_prod / profit * 100) if profit > 0 else 0
                print(f"   • {produit.nom:20s} : {quantite:10.2f} unités "
                      f"→ Profit: {profit_prod:10.2f} ({pct_profit:5.1f}%)")
            else:
                print(f"   • {produit.nom:20s} : {quantite:10.2f} (Non produit)")
        
        # Profit total
        print(f"\n💰 Profit total maximal : {profit:.2f} devises")
        
        # Utilisation des ressources
        ressources_utilisees = probleme.calculer_ressources_utilisees(solution)
        
        print(f"\n♻️  Utilisation des ressources :")
        
        resources_data = [
            ('Lait', ressources_utilisees['lait'], ressources.lait_disponible),
            ('Machine', ressources_utilisees['machine'], ressources.heures_machine_disponibles),
            ('Main d\'œuvre', ressources_utilisees['main_oeuvre'], ressources.heures_main_oeuvre_disponibles)
        ]
        
        for nom, utilisee, disponible in resources_data:
            pct = (utilisee / disponible * 100) if disponible > 0 else 0
            barre = "█" * int(pct / 5) + "░" * (20 - int(pct / 5))
            saturee = " [✓ SATURÉE - GOULOT]" if pct > 99 else " [Non saturée]"
            
            print(f"\n   {nom}:")
            print(f"   Utilisée   : {utilisee:7.2f} {'/'.join([u for u in ['L', 'h', 'h']][:1]) if nom == 'Lait' else 'h' if nom == 'Machine' else 'h'}")
            print(f"   Disponible : {disponible:7.2f}")
            print(f"   Taux       : {pct:6.1f}% {barre}{saturee}")
        
        # Analyse de sensibilité
        print(f"\n🔍 ANALYSE DE SENSIBILITÉ :")
        print("-" * 70)
        
        print("\n   📌 Interprétation des résultats:")
        
        # Identifier les goulots
        ressources_saturees = []
        for nom, utilisee, disponible in resources_data:
            pct = (utilisee / disponible * 100) if disponible > 0 else 0
            if pct > 99:
                ressources_saturees.append(nom)
        
        if ressources_saturees:
            print(f"\n   ⚠️  Ressources LIMITANTes (saturées) :")
            for res in ressources_saturees:
                print(f"      • {res}")
            print(f"\n      Action recommandée: AUGMENTER ces ressources")
            print(f"      pour améliorer le profit optimal.")
        
        # Ressources libres
        ressources_libres = []
        for nom, utilisee, disponible in resources_data:
            pct = (utilisee / disponible * 100) if disponible > 0 else 0
            if pct < 95:
                ressources_libres.append((nom, pct))
        
        if ressources_libres:
            print(f"\n   ✓ Ressources EXCÉDENTAIRES (non saturées) :")
            for res, pct in ressources_libres:
                excedent_pct = 100 - pct
                print(f"      • {res}: {excedent_pct:.1f}% inutilisé")
            print(f"\n      Action recommandée: RÉDUIRE ces ressources")
            print(f"      ne changera pas le profit optimal.")
        
        # Produits sans production
        produits_non_produits = []
        for produit in produits:
            quantite = solution.get(produit.nom, 0)
            if quantite < 1e-6:
                produits_non_produits.append(produit)
        
        if produits_non_produits:
            print(f"\n   ❌ Produits NON RENTABLES (non produits) :")
            for produit in produits_non_produits:
                print(f"      • {produit.nom}")
            print(f"\n      Raison: Pas assez de ressources après")
            print(f"              les produits plus rentables.")
            print(f"      Action: Améliorer la profitabilité ou")
            print(f"              augmenter les ressources.")
    
    else:
        print(f"\n❌ Pas de solution trouvée. Statut: {solveur.statut}")
    
    # ========== CONCLUSION ==========
    
    afficher_separation("=")
    print("\n✨ DÉMONSTRATION COMPLÈTE")
    print("="*70)
    
    print("\n📚 Concepts démontrés :")
    print("   1. ✓ Programmation Orientée Objet")
    print("      - Classes abstraites (Produit)")
    print("      - Héritage (Lait, Yaourt, Fromage)")
    print("      - Polymorphisme (calcul_profit, consommation_lait, etc.)")
    print("      - Encapsulation (getters/setters)")
    print()
    print("   2. ✓ Modélisation mathématique")
    print("      - Variables de décision")
    print("      - Fonction objectif")
    print("      - Contraintes")
    print()
    print("   3. ✓ Programmation linéaire")
    print("      - Formulation du problème")
    print("      - Résolution optimale")
    print()
    print("   4. ✓ Algorithme du Simplexe")
    print("      - Utilisation de PuLP + CBC")
    print("      - Garantie de l'optimalité")
    print("      - Analyse de sensibilité")
    print()
    print("   5. ✓ Recherche Opérationnelle pratique")
    print("      - Application réelle")
    print("      - Prise de décision")
    print("      - Optimisation des ressources")
    
    print("\n" + "="*70)
    print("👉 Pour utiliser l'application interactive :")
    print("   python main.py")
    print("="*70 + "\n")


if __name__ == "__main__":
    try:
        demo_complete()
    except Exception as e:
        print(f"\n❌ Erreur: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
