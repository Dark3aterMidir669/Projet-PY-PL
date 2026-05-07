"""
Module product.py : Implémentation des classes de produits laitiers.

Ce module contient :
- Classe abstraite Produit
- Classes dérivées : Lait, Yaourt, Fromage
- Polymorphisme : chaque produit implémente ses propres calculs de ressources
"""

from abc import ABC, abstractmethod


class Produit(ABC):
    """
    Classe abstraite représentant un produit laitier.
    
    Attributes:
        _nom (str): Nom du produit
        _cout_unitaire (float): Coût de production unitaire (en devises)
        _prix_vente_unitaire (float): Prix de vente unitaire (en devises)
        _profit_unitaire (float): Profit unitaire = prix - coût
    """
    
    def __init__(self, nom: str, cout_unitaire: float, prix_vente_unitaire: float):
        """
        Initialise un produit avec ses paramètres économiques.
        
        Args:
            nom (str): Nom du produit
            cout_unitaire (float): Coût de production unitaire
            prix_vente_unitaire (float): Prix de vente unitaire
            
        Raises:
            ValueError: Si les coûts sont négatifs ou le prix < coût
        """
        if cout_unitaire < 0 or prix_vente_unitaire < 0:
            raise ValueError("Les coûts et prix doivent être positifs")
        if prix_vente_unitaire < cout_unitaire:
            raise ValueError(f"Le prix de vente ({prix_vente_unitaire}) "
                           f"doit être >= au coût ({cout_unitaire})")
        
        self._nom = nom
        self._cout_unitaire = cout_unitaire
        self._prix_vente_unitaire = prix_vente_unitaire
        self._profit_unitaire = prix_vente_unitaire - cout_unitaire
    
    # ========== PROPRIÉTÉS (Getters) ==========
    
    @property
    def nom(self) -> str:
        """Retourne le nom du produit (encapsulation en lecture)."""
        return self._nom
    
    @property
    def cout_unitaire(self) -> float:
        """Retourne le coût unitaire."""
        return self._cout_unitaire
    
    @property
    def prix_vente_unitaire(self) -> float:
        """Retourne le prix de vente unitaire."""
        return self._prix_vente_unitaire
    
    @property
    def profit_unitaire(self) -> float:
        """Retourne le profit unitaire."""
        return self._profit_unitaire
    
    # ========== SETTERS ==========
    
    @cout_unitaire.setter
    def cout_unitaire(self, valeur: float):
        """Modifie le coût unitaire et recalcule le profit."""
        if valeur < 0:
            raise ValueError("Le coût doit être positif")
        self._cout_unitaire = valeur
        self._profit_unitaire = self._prix_vente_unitaire - valeur
    
    @prix_vente_unitaire.setter
    def prix_vente_unitaire(self, valeur: float):
        """Modifie le prix de vente et recalcule le profit."""
        if valeur < 0:
            raise ValueError("Le prix doit être positif")
        if valeur < self._cout_unitaire:
            raise ValueError(f"Le prix ({valeur}) doit être >= au coût ({self._cout_unitaire})")
        self._prix_vente_unitaire = valeur
        self._profit_unitaire = valeur - self._cout_unitaire
    
    # ========== MÉTHODES ABSTRAITES ==========
    
    @abstractmethod
    def consommation_lait(self) -> float:
        """
        Retourne la quantité de lait (en litres) nécessaire pour produire 1 unité.
        Doit être implémentée par chaque classe dérivée.
        
        Returns:
            float: Litres de lait par unité produite
        """
        pass
    
    @abstractmethod
    def temps_machine(self) -> float:
        """
        Retourne le temps machine (en heures) nécessaire pour produire 1 unité.
        
        Returns:
            float: Heures de machine par unité produite
        """
        pass
    
    @abstractmethod
    def temps_main_oeuvre(self) -> float:
        """
        Retourne le temps de main d'œuvre (en heures) pour produire 1 unité.
        
        Returns:
            float: Heures de main d'œuvre par unité produite
        """
        pass
    
    @abstractmethod
    def calcul_profit(self, quantite: float) -> float:
        """
        Calcule le profit total pour une quantité donnée.
        Méthode polymorphe : implémentation spécifique à chaque produit.
        
        Args:
            quantite (float): Quantité à produire
            
        Returns:
            float: Profit total
        """
        pass
    
    @abstractmethod
    def __str__(self) -> str:
        """Représentation textuelle du produit."""
        pass


class Lait(Produit):
    """
    Classe représentant le produit 'Lait en sachet'.
    
    Paramètres de production :
    - Lait : 1.0 litre par sachet
    - Machine : 0.1 heure par sachet
    - Main d'œuvre : 0.05 heure par sachet
    """
    
    def __init__(self, cout_unitaire: float = 0.3, prix_vente_unitaire: float = 0.8):
        """
        Initialise le produit Lait avec ses paramètres par défaut.
        
        Args:
            cout_unitaire (float): Coût unitaire en devises (défaut: 0.3)
            prix_vente_unitaire (float): Prix de vente en devises (défaut: 0.8)
        """
        super().__init__("Lait en sachet", cout_unitaire, prix_vente_unitaire)
    
    def consommation_lait(self) -> float:
        """Retourne la consommation de lait : 1 litre par sachet."""
        return 1.0
    
    def temps_machine(self) -> float:
        """Retourne le temps machine : 0.1 heure par sachet."""
        return 0.1
    
    def temps_main_oeuvre(self) -> float:
        """Retourne la main d'œuvre : 0.05 heure par sachet."""
        return 0.05
    
    def calcul_profit(self, quantite: float) -> float:
        """
        Calcule le profit du lait en sachet.
        Le profit est simple : profit_unitaire * quantite
        
        Args:
            quantite (float): Nombre de sachets
            
        Returns:
            float: Profit total
        """
        return self._profit_unitaire * quantite
    
    def __str__(self) -> str:
        """Représentation textuelle du Lait."""
        return (f"Lait en sachet | Coût: {self._cout_unitaire:.2f} | "
                f"Prix: {self._prix_vente_unitaire:.2f} | Profit: {self._profit_unitaire:.2f}")


class Yaourt(Produit):
    """
    Classe représentant le produit 'Yaourt'.
    
    Paramètres de production :
    - Lait : 1.5 litres par pot
    - Machine : 0.2 heure par pot (processus de fermentation)
    - Main d'œuvre : 0.1 heure par pot
    """
    
    def __init__(self, cout_unitaire: float = 0.6, prix_vente_unitaire: float = 1.5):
        """
        Initialise le produit Yaourt avec ses paramètres par défaut.
        
        Args:
            cout_unitaire (float): Coût unitaire en devises (défaut: 0.6)
            prix_vente_unitaire (float): Prix de vente en devises (défaut: 1.5)
        """
        super().__init__("Yaourt", cout_unitaire, prix_vente_unitaire)
    
    def consommation_lait(self) -> float:
        """Retourne la consommation de lait : 1.5 litres par pot."""
        return 1.5
    
    def temps_machine(self) -> float:
        """Retourne le temps machine : 0.2 heure par pot."""
        return 0.2
    
    def temps_main_oeuvre(self) -> float:
        """Retourne la main d'œuvre : 0.1 heure par pot."""
        return 0.1
    
    def calcul_profit(self, quantite: float) -> float:
        """
        Calcule le profit du yaourt.
        Le profit inclut une légère prime pour la transformation.
        
        Args:
            quantite (float): Nombre de pots
            
        Returns:
            float: Profit total
        """
        profit_base = self._profit_unitaire * quantite
        # Prime de transformation : 5% du profit de base
        prime_transformation = profit_base * 0.05
        return profit_base + prime_transformation
    
    def __str__(self) -> str:
        """Représentation textuelle du Yaourt."""
        return (f"Yaourt | Coût: {self._cout_unitaire:.2f} | "
                f"Prix: {self._prix_vente_unitaire:.2f} | Profit: {self._profit_unitaire:.2f}")


class Fromage(Produit):
    """
    Classe représentant le produit 'Fromage'.
    
    Paramètres de production :
    - Lait : 3.0 litres par kg (rapport de concentration)
    - Machine : 0.5 heure par kg
    - Main d'œuvre : 0.3 heure par kg
    """
    
    def __init__(self, cout_unitaire: float = 1.5, prix_vente_unitaire: float = 4.5):
        """
        Initialise le produit Fromage avec ses paramètres par défaut.
        
        Args:
            cout_unitaire (float): Coût unitaire en devises (défaut: 1.5)
            prix_vente_unitaire (float): Prix de vente en devises (défaut: 4.5)
        """
        super().__init__("Fromage", cout_unitaire, prix_vente_unitaire)
    
    def consommation_lait(self) -> float:
        """Retourne la consommation de lait : 3 litres par kg de fromage."""
        return 3.0
    
    def temps_machine(self) -> float:
        """Retourne le temps machine : 0.5 heure par kg."""
        return 0.5
    
    def temps_main_oeuvre(self) -> float:
        """Retourne la main d'œuvre : 0.3 heure par kg."""
        return 0.3
    
    def calcul_profit(self, quantite: float) -> float:
        """
        Calcule le profit du fromage.
        Le fromage a une plus haute valeur ajoutée.
        Prime de transformation : 10% du profit de base.
        
        Args:
            quantite (float): Nombre de kg
            
        Returns:
            float: Profit total
        """
        profit_base = self._profit_unitaire * quantite
        # Prime de transformation : 10% du profit de base
        prime_transformation = profit_base * 0.10
        return profit_base + prime_transformation
    
    def __str__(self) -> str:
        """Représentation textuelle du Fromage."""
        return (f"Fromage | Coût: {self._cout_unitaire:.2f} | "
                f"Prix: {self._prix_vente_unitaire:.2f} | Profit: {self._profit_unitaire:.2f}")
