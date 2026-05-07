"""
main.py : Point d'entrée de l'application ProPytho.

APPLICATION COMPLÈTE D'OPTIMISATION LINÉAIRE
============================================

Objectif:
    Optimiser la marge bénéficiaire d'une unité de transformation laitière
    en utilisant la programmation linéaire et l'algorithme du Simplexe.

Architecture:
    - models/ : Définition des produits et ressources (POO)
    - solver/ : Modélisation et résolution du problème (Simplexe)
    - ui/ : Interface utilisateur (CLI)
    - utils/ : Fonctions utilitaires

Flux principal:
    1. Application lance le menu
    2. Utilisateur initialise les données
    3. Création du problème d'optimisation
    4. Résolution par le Simplexe (PuLP + CBC)
    5. Affichage des résultats et analyse

Concepts POO utilisés:
    ✓ Classes abstraites (Produit)
    ✓ Héritage (Lait, Yaourt, Fromage hérient de Produit)
    ✓ Polymorphisme (chaque produit redéfinit consommation_lait, etc.)
    ✓ Encapsulation (attributs privés + getters/setters)
    ✓ Séparation des responsabilités (models, solver, ui)

Concepts de RO:
    ✓ Programmation linéaire
    ✓ Variables de décision
    ✓ Fonction objectif (maximisation de profit)
    ✓ Contraintes (ressources)
    ✓ Algorithme du Simplexe
    ✓ Analyse de sensibilité

Author: ProPytho Project
Date: 2025
"""

import sys
from ui import Application
from utils import afficher_info_systeme


def main():
    """Fonction principale."""
    
    try:
        # Créer et lancer l'application
        app = Application()
        app.run()
    
    except KeyboardInterrupt:
        print("\n\n⚠️  Application interrompue par l'utilisateur.")
        sys.exit(0)
    
    except Exception as e:
        print(f"\n❌ Erreur fatale : {str(e)}")
        print("\nTips de dépannage :")
        print("1. Vérifiez que les dépendances sont installées :")
        print("   pip install -r requirements.txt")
        print("\n2. Vérifiez la version de Python (3.7+)")
        afficher_info_systeme()
        sys.exit(1)


if __name__ == "__main__":
    main()
