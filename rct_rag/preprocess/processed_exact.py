"""
processed_exact.py

Ce module contient les fonctions de prétraitement utilisées pour la recherche exacte.

Fonctions :
- preprocess_ex(text) : nettoie un texte en le mettant en minuscules et en supprimant la ponctuation.
- preprocess_query(query) : applique le nettoyage à une requête utilisateur.
"""

import re

def preprocess_ex(text):
    # Met en minuscules
    text = text.lower()

    # Remplace les caractères de ponctuation (sauf * et -) par un espace
    text = re.sub(r'[^\w\s*-]|_', ' ', text)

    #Supprime les tirets pour créer : double-mots = doublemots 
    text = text.replace("-", "")

    return text

def preprocess_query(query):
    query_cleaned = preprocess_ex(query)
    return query_cleaned
