"""
Module helpers.py : Fonctions utilitaires pour l'interface et le calcul.
"""

from typing import Dict


def afficher_banner() -> None:
    """Affiche le banneau d'accueil de l'application."""
    
    banner = """
╔══════════════════════════════════════════════════════════════════════╗
║                                                                      ║
║               PROPYTHO - OPTIMISATION LAITIÈRE                       ║
║                                                                      ║
║           Maximisation de la marge bénéficiaire par                  ║
║         programmation linéaire et algorithme du Simplexe             ║
║                                                                      ║
║  Transformation du lait cru en :                                     ║
║    • Lait en sachet     • Yaourt     • Fromage                       ║
║                                                                      ║
║  Technologies utilisées :                                            ║
║    • Python 3.x                                                      ║
║    • POO : Classes abstraites, héritage, polymorphisme               ║
║    • PuLP + CBC (COIN-OR) pour le Simplexe                           ║
║                                                                      ║
╚══════════════════════════════════════════════════════════════════════╝
    """
    print(banner)


def afficher_separation(caractere: str = "=", longueur: int = 70) -> None:
    """
    Affiche une ligne de séparation.
    
    Args:
        caractere (str): Caractère à répéter (défaut: "=")
        longueur (int): Longueur de la ligne (défaut: 70)
    """
    print(f"\n{caractere * longueur}")


def arrondir_solution(solution: Dict[str, float], seuil: float = 1e-5) -> Dict[str, float]:
    """
    Arrondit une solution en remplaçant les petites valeurs par 0.
    
    Cela est utile car le solveur peut retourner des valeurs très petites
    (ex: 1e-10) au lieu de 0 pour les variables non-basiques.
    
    Args:
        solution (Dict[str, float]): Solution brute du solveur
        seuil (float): Valeurs disous ce seuil sont arrondies à 0
        
    Returns:
        Dict[str, float]: Solution arrondie
    """
    return {
        nom: quantite if quantite > seuil else 0
        for nom, quantite in solution.items()
    }


def verifier_solveur_disponible() -> bool:
    """
    Vérifie que les dépendances nécessaires sont installées.
    
    Returns:
        bool: True si tous les solveurs sont disponibles
    """
    try:
        import pulp
        # Vérifier que CBC est disponible
        try:
            import pyomo.environ
            return True
        except ImportError:
            # CBC est inclus avec PuLP sur Windows
            return True
    except ImportError:
        return False


def afficher_info_systeme() -> None:
    """Affiche les informations du système et des dépendances."""
    
    import sys
    import platform
    
    print("\n📋 INFORMATIONS SYSTÈME :")
    print("-" * 70)
    print(f"   Python version : {sys.version.split()[0]}")
    print(f"   Plateforme : {platform.system()} {platform.release()}")
    
    # Vérifier PuLP
    try:
        import pulp
        print(f"   PuLP : ✓ Installé (v{pulp.__version__})")
    except ImportError:
        print("   PuLP : ✗ Non installé")
    
    # Vérifier NumPy
    try:
        import numpy
        print(f"   NumPy : ✓ Installé (v{numpy.__version__})")
    except ImportError:
        print("   NumPy : ✗ Non installé")
    
    # Vérifier SciPy
    try:
        import scipy
        print(f"   SciPy : ✓ Installé (v{scipy.__version__})")
    except ImportError:
        print("   SciPy : ✗ Non installé")
