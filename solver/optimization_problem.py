"""
Module optimization_problem.py : Modélisation du problème d'optimisation.

Classe ProblemeOptimisation :
- Agrège les variables de décision
- Définit la fonction objectif
- Définit les contraintes
- Prépare le problème pour le solveur
"""

from typing import List, Dict, Tuple
from models import Produit, Ressource


class ProblemeOptimisation:
    """
    Classe représentant le problème d'optimisation linéaire.
    
    Attributes:
        _produits (List[Produit]): Liste des produits à optimiser
        _ressources (Ressource): Ressources disponibles
        _coefficients_objective (Dict): Coefficients de la fonction objectif
        _contraintes (Dict): Dictionnaire des contraintes
    """
    
    def __init__(self, produits: List[Produit], ressources: Ressource):
        """
        Initialise le problème d'optimisation.
        
        Args:
            produits (List[Produit]): Liste des produits
            ressources (Ressource): Ressources disponibles
        """
        self._produits = produits
        self._ressources = ressources
        self._coefficients_objective = {}
        self._contraintes = {}
        
        # Initialise les coefficients de la fonction objectif
        self._initialiser_fonction_objectif()
        # Initialise les contraintes
        self._initialiser_contraintes()
    
    def _initialiser_fonction_objectif(self) -> None:
        """
        Initialise les coefficients de la fonction objectif.
        Chaque coefficient est le profit unitaire du produit.
        
        Pour la maximisation de profit :
        Maximiser : sum(profit_i * x_i)
        où x_i est la quantité du produit i
        """
        for produit in self._produits:
            self._coefficients_objective[produit.nom] = produit.profit_unitaire
    
    def _initialiser_contraintes(self) -> None:
        """
        Initialise les contraintes du problème.
        
        Contraintes :
        1. Lait : sum(consommation_lait_i * x_i) <= lait_disponible
        2. Machine : sum(temps_machine_i * x_i) <= heures_machine
        3. Main d'œuvre : sum(temps_main_oeuvre_i * x_i) <= heures_main_oeuvre
        4. Non-négativité : x_i >= 0 (géré automatiquement par le solveur)
        """
        
        # Contrainte 1 : Disponibilité du lait
        self._contraintes['lait'] = {
            'coefficients': {produit.nom: produit.consommation_lait() 
                            for produit in self._produits},
            'limite': self._ressources.lait_disponible,
            'description': 'Disponibilité du lait (litres)'
        }
        
        # Contrainte 2 : Disponibilité machine
        self._contraintes['machine'] = {
            'coefficients': {produit.nom: produit.temps_machine() 
                            for produit in self._produits},
            'limite': self._ressources.heures_machine_disponibles,
            'description': 'Disponibilité machine (heures)'
        }
        
        # Contrainte 3 : Disponibilité main d'œuvre
        self._contraintes['main_oeuvre'] = {
            'coefficients': {produit.nom: produit.temps_main_oeuvre() 
                            for produit in self._produits},
            'limite': self._ressources.heures_main_oeuvre_disponibles,
            'description': 'Disponibilité main d\'œuvre (heures)'
        }
    
    # ========== PROPRIÉTÉS ==========
    
    @property
    def produits(self) -> List[Produit]:
        """Retourne la liste des produits."""
        return self._produits
    
    @property
    def ressources(self) -> Ressource:
        """Retourne les ressources."""
        return self._ressources
    
    @property
    def coefficients_objective(self) -> Dict:
        """Retourne les coefficients de la fonction objectif."""
        return self._coefficients_objective
    
    @property
    def contraintes(self) -> Dict:
        """Retourne les contraintes."""
        return self._contraintes
    
    # ========== MÉTHODES PUBLIQUES ==========
    
    def afficher_modele(self) -> None:
        """Affiche la formulation mathématique du problème."""
        print("\n" + "="*70)
        print("MODÉLISATION DU PROBLÈME D'OPTIMISATION")
        print("="*70)
        
        # Fonction objectif
        print("\nFONCTION OBJECTIF (Maximiser le profit) :")
        print("-" * 70)
        termes_obj = [f"{coeff:.4f}*{nom}" 
                     for nom, coeff in self._coefficients_objective.items()]
        print(f"Maximiser : {' + '.join(termes_obj)}")
        
        # Contraintes
        print("\n\nCONTRAINTES :")
        print("-" * 70)
        
        for contrainte_nom, contrainte_data in self._contraintes.items():
            coeffs = contrainte_data['coefficients']
            limite = contrainte_data['limite']
            desc = contrainte_data['description']
            
            termes = [f"{coeff:.4f}*{nom}" for nom, coeff in coeffs.items()]
            print(f"\n{desc} :")
            print(f"  {' + '.join(termes)} <= {limite:.2f}")
        
        print("\n\nCONTRAINTES DE POSITIVITÉ :")
        print("-" * 70)
        for produit in self._produits:
            print(f"  {produit.nom} >= 0")
        
        print("\n" + "="*70)
    
    def get_variable_names(self) -> List[str]:
        """
        Retourne la liste des noms de variables de décision.
        
        Returns:
            List[str]: Noms des produits (variables)
        """
        return [produit.nom for produit in self._produits]
    
    def calculer_ressources_utilisees(self, solution: Dict[str, float]) -> Dict[str, float]:
        """
        Calcule les ressources utilisées pour une solution donnée.
        
        Args:
            solution (Dict[str, float]): Dictionnaire {produit_nom: quantité}
            
        Returns:
            Dict[str, float]: Ressources utilisées
        """
        ressources_utilisees = {
            'lait': 0,
            'machine': 0,
            'main_oeuvre': 0
        }
        
        for produit in self._produits:
            if produit.nom in solution:
                quantite = solution[produit.nom]
                ressources_utilisees['lait'] += produit.consommation_lait() * quantite
                ressources_utilisees['machine'] += produit.temps_machine() * quantite
                ressources_utilisees['main_oeuvre'] += produit.temps_main_oeuvre() * quantite
        
        return ressources_utilisees
    
    def verifier_contraintes(self, solution: Dict[str, float]) -> bool:
        """
        Vérifie si une solution respecte toutes les contraintes.
        
        Args:
            solution (Dict[str, float]): Dictionnaire {produit_nom: quantité}
            
        Returns:
            bool: True si toutes les contraintes sont respectées
        """
        ressources_utilisees = self.calculer_ressources_utilisees(solution)
        
        # Vérifier lait
        if ressources_utilisees['lait'] > self._ressources.lait_disponible + 1e-6:
            return False
        
        # Vérifier machine
        if ressources_utilisees['machine'] > self._ressources.heures_machine_disponibles + 1e-6:
            return False
        
        # Vérifier main d'œuvre
        if ressources_utilisees['main_oeuvre'] > self._ressources.heures_main_oeuvre_disponibles + 1e-6:
            return False
        
        # Vérifier positivité
        for quantite in solution.values():
            if quantite < -1e-6:
                return False
        
        return True
