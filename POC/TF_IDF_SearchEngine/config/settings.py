"""
settings.py

Ce module contient les paramètres de configuration globaux utilisés par les différents composants
de l’application de recherche documentaire.

Paramètres définis :
- TOP_K_RESULTS : Nombre de résultats à retourner après une requête (valeur par défaut : 10).
- EMBEDDING_MODEL_NAME : Nom du modèle d’embedding utilisé pour la recherche dense.

Ces paramètres permettent d'ajuster facilement le comportement du moteur de recherche sans modifier le code principal.
"""


# Nombre de résultats à retourner
TOP_K_RESULTS = 20

TOP_K_MOTS = 3