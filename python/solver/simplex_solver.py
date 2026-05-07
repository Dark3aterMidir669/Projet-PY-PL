"""
Module simplex_solver.py : Résolution du problème d'optimisation.

Utilise la bibliothèque PuLP pour implémenter la méthode du Simplexe.
PuLP formule le problème et utilise le solveur COIN-OR (CBC) par défaut,
qui implémente l'algorithme du Simplexe pour la programmation linéaire.
"""

from typing import Dict, Tuple, Optional
import pulp
from .optimization_problem import ProblemeOptimisation


class SimplexeSolver:
    """
    Solveur utilisant la méthode du Simplexe via PuLP.
    
    Résout les problèmes de programmation linéaire en utilisant l'algorithme
    du Simplexe implémenté dans le solveur CBC de COIN-OR.
    
    Attributes:
        _probleme (ProblemeOptimisation): Problème à résoudre
        _problem_pulp (pulp.LpProblem): Problème PuLP
        _variables (Dict): Variables de décision PuLP
        _solution (Optional[Dict]): Dernière solution calculée
        _statut (Optional[str]): Statut de la dernière résolution
    """
    
    def __init__(self, probleme: ProblemeOptimisation):
        """
        Initialise le solveur.
        
        Args:
            probleme (ProblemeOptimisation): Problème à résoudre
        """
        self._probleme = probleme
        self._problem_pulp = None
        self._variables = {}
        self._solution = None
        self._statut = None
        self._profit_optimal = None
    
    def _construire_probleme_pulp(self) -> None:
        """
        Construit le problème PuLP à partir du problème d'optimisation.
        
        Crée :
        1. Les variables de décision (variables continues >= 0)
        2. La fonction objectif
        3. Les contraintes
        """
        
        # Crée un problème de maximisation
        self._problem_pulp = pulp.LpProblem("Optimisation_Laiterie", pulp.LpMaximize)
        
        # Crée les variables de décision (continues et positives par défaut)
        noms_variables = self._probleme.get_variable_names()
        for nom in noms_variables:
            self._variables[nom] = pulp.LpVariable(nom, lowBound=0, cat='Continuous')
        
        # Ajoute la fonction objectif
        objectif = pulp.lpSum([
            self._probleme.coefficients_objective[nom] * self._variables[nom]
            for nom in noms_variables
        ])
        self._problem_pulp += objectif, "Profit_Total"
        
        # Ajoute les contraintes
        contraintes = self._probleme.contraintes
        
        # Contrainte de lait
        self._problem_pulp += (
            pulp.lpSum([
                contraintes['lait']['coefficients'][nom] * self._variables[nom]
                for nom in noms_variables
            ]) <= contraintes['lait']['limite'],
            "Contrainte_Lait"
        )
        
        # Contrainte de machine
        self._problem_pulp += (
            pulp.lpSum([
                contraintes['machine']['coefficients'][nom] * self._variables[nom]
                for nom in noms_variables
            ]) <= contraintes['machine']['limite'],
            "Contrainte_Machine"
        )
        
        # Contrainte de main d'œuvre
        self._problem_pulp += (
            pulp.lpSum([
                contraintes['main_oeuvre']['coefficients'][nom] * self._variables[nom]
                for nom in noms_variables
            ]) <= contraintes['main_oeuvre']['limite'],
            "Contrainte_Main_Oeuvre"
        )
    
    def resoudre(self, verbose: bool = False) -> Tuple[bool, Dict[str, float], float]:
        """
        Résout le problème en utilisant l'algorithme du Simplexe.
        
        EXPLICATION TECHNIQUE DE L'ALGORITHME DU SIMPLEXE :
        ====================================================
        
        Le Simplexe est un algorithme itératif qui :
        
        1. Démarre à un sommet réalisable du polytope des contraintes
        2. À chaque itération, se déplace vers un sommet voisin améliorant l'objectif
        3. S'arrête quand aucun déplacement ne peut améliorer l'objectif
        
        Étapes principales :
        a) Conversion en forme standard (tableaux augmentés)
        b) Initialisation : trouver une solution réalisable de base
        c) Boucle d'itération :
           - Sélectionner la variable entrante (direction d'amélioration)
           - Sélectionner la variable sortante (limite de positivité)
           - Pivoter le tableau
           - Vérifier l'optimalité
        
        Avantage : Très efficace en pratique pour les problèmes LP.
        Complexité théorique : Exponentielle but temps polynomial en moyenne.
        
        Args:
            verbose (bool): Si True, affiche les détails de la résolution
            
        Returns:
            Tuple[bool, Dict, float]: (Succès, Solution, Profit optimal)
                - bool: True si une solution optimale a été trouvée
                - Dict: {produit_nom: quantité_optimale}
                - float: Valeur de la fonction objectif (profit maximal)
        """
        
        # Construire le problème PuLP
        self._construire_probleme_pulp()
        
        if verbose:
            print("\n[SOLVEUR] Construction du problème : OK")
            print(f"[SOLVEUR] Nombre de variables : {len(self._variables)}")
            print(f"[SOLVEUR] Nombre de contraintes : {len(self._problem_pulp.constraints)}")
        
        # Résoudre le problème sans message PuLP
        self._problem_pulp.solve(pulp.PULP_CBC_CMD(msg=0))
        
        # Récupérer le statut
        self._statut = pulp.LpStatus[self._problem_pulp.status]
        
        if verbose:
            print(f"[SOLVEUR] Statut de résolution : {self._statut}")
        
        # Vérifier si la solution est optimale
        if self._statut != 'Optimal':
            return False, {}, 0
        
        # Extraire la solution
        self._solution = {
            nom: var.varValue if var.varValue is not None else 0
            for nom, var in self._variables.items()
        }
        
        # Profit optimal (arrondir les petites valeurs)
        self._profit_optimal = pulp.value(self._problem_pulp.objective)
        
        return True, self._solution, self._profit_optimal
    
    def afficher_details_resolution(self) -> None:
        """Affiche les détails techniques de la résolution."""
        if self._problem_pulp is None:
            print("Aucun problème résolu. Appelez resoudre() d'abord.")
            return
        
        print("\n" + "="*70)
        print("DÉTAILS DE LA RÉSOLUTION (ALGORITHME SIMPLEXE)")
        print("="*70)
        
        print(f"\nStatut final : {self._statut}")
        
        if self._statut == 'Optimal':
            print("\n✓ Solution optimale trouvée par l'algorithme du Simplexe.")
            print("\nInterprétation :")
            print("  - L'algorithme a itéré à travers les sommets du polytope")
            print("  - À chaque itération, il s'est déplacé vers un sommet adjacent")
            print("  - Qui améliore la fonction objectif")
            print("  - Jusqu'à atteindre un sommet optimal (aucun voisin meilleur)")
            print("\nProoriétés :")
            print("  - La solution est un sommet du polytope des contraintes")
            print("  - C'est une solution de base (au plus N variables non-nulles)")
            print("  - Aucune autre solution ne peut donner un meilleur objectif")
        else:
            print(f"\n✗ Pas de solution optimale. Statut : {self._statut}")
    
    @property
    def solution(self) -> Optional[Dict[str, float]]:
        """Retourne la dernière solution calculée."""
        return self._solution
    
    @property
    def profit_optimal(self) -> Optional[float]:
        """Retourne le profit optimal."""
        return self._profit_optimal
    
    @property
    def statut(self) -> Optional[str]:
        """Retourne le statut de la résolution."""
        return self._statut
