"""
Module resource.py : Classe de gestion des ressources de production.

Gère les contraintes de ressources disponibles :
- Lait disponible (litres)
- Heures machine disponibles
- Heures de main d'œuvre disponibles
"""


class Ressource:
    """
    Classe représentant les ressources disponibles pour la production.
    
    Attributes:
        _lait_disponible (float): Quantité de lait disponible en litres
        _heures_machine_disponibles (float): Heures de machine disponibles
        _heures_main_oeuvre_disponibles (float): Heures de main d'œuvre disponibles
    """
    
    def __init__(self, lait_disponible: float, heures_machine: float, 
                 heures_main_oeuvre: float):
        """
        Initialise les ressources disponibles.
        
        Args:
            lait_disponible (float): Litres de lait disponibles
            heures_machine (float): Heures de machine disponibles
            heures_main_oeuvre (float): Heures de main d'œuvre disponibles
            
        Raises:
            ValueError: Si les ressources sont négatives
        """
        if lait_disponible < 0 or heures_machine < 0 or heures_main_oeuvre < 0:
            raise ValueError("Les ressources doivent être positives")
        
        self._lait_disponible = lait_disponible
        self._heures_machine_disponibles = heures_machine
        self._heures_main_oeuvre_disponibles = heures_main_oeuvre
    
    # ========== PROPRIÉTÉS (Getters) ==========
    
    @property
    def lait_disponible(self) -> float:
        """Retourne la quantité de lait disponible."""
        return self._lait_disponible
    
    @property
    def heures_machine_disponibles(self) -> float:
        """Retourne les heures machine disponibles."""
        return self._heures_machine_disponibles
    
    @property
    def heures_main_oeuvre_disponibles(self) -> float:
        """Retourne les heures de main d'œuvre disponibles."""
        return self._heures_main_oeuvre_disponibles
    
    # ========== SETTERS ==========
    
    @lait_disponible.setter
    def lait_disponible(self, valeur: float):
        """Modifie la quantité de lait disponible."""
        if valeur < 0:
            raise ValueError("Le lait disponible doit être positif")
        self._lait_disponible = valeur
    
    @heures_machine_disponibles.setter
    def heures_machine_disponibles(self, valeur: float):
        """Modifie les heures machine disponibles."""
        if valeur < 0:
            raise ValueError("Les heures machine disponibles doivent être positives")
        self._heures_machine_disponibles = valeur
    
    @heures_main_oeuvre_disponibles.setter
    def heures_main_oeuvre_disponibles(self, valeur: float):
        """Modifie les heures de main d'œuvre disponibles."""
        if valeur < 0:
            raise ValueError("Les heures de main d'œuvre doivent être positives")
        self._heures_main_oeuvre_disponibles = valeur
    
    def __str__(self) -> str:
        """Représentation textuelle des ressources."""
        return (f"Ressources disponibles:\n"
                f"  - Lait: {self._lait_disponible:.2f} litres\n"
                f"  - Machine: {self._heures_machine_disponibles:.2f} heures\n"
                f"  - Main d'œuvre: {self._heures_main_oeuvre_disponibles:.2f} heures")
    
    def to_dict(self) -> dict:
        """
        Retourne un dictionnaire des ressources.
        
        Returns:
            dict: Ressources sous forme de dictionnaire
        """
        return {
            'lait': self._lait_disponible,
            'machine': self._heures_machine_disponibles,
            'main_oeuvre': self._heures_main_oeuvre_disponibles
        }
