"""
Module models : Contient les classes de modélisation des produits et ressources.
"""

from .product import Produit, Lait, Yaourt, Fromage
from .resource import Ressource

__all__ = ['Produit', 'Lait', 'Yaourt', 'Fromage', 'Ressource']
