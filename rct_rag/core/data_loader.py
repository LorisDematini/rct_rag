"""
data_loader.py

Ce module gère le chargement des données pour les deux types de moteur de recherche :
- Recherche exacte
- Recherche sémantique/TF-IDF

Fonctions principales :
- load_data_sparse() :
    Charge les documents pour la recherche sparse.
    Si le fichier JSON n’existe pas, il est généré via document_sparse().

- load_data_exact() :
    Charge les documents pour la recherche exacte.
    Si le fichier JSON n’existe pas, il est généré via document_exact().
"""

import os
from config.paths import EXACT_JSON_PATH, SPARSE_JSON_PATH
from core.document_loader import document_exact, document_sparse


def load_data_sparse():
     #Si pas de sauvegarde en crée une, sinon la charge
    if not os.path.exists(SPARSE_JSON_PATH):
        print(f"[INFO] Le fichier SPARSE_JSON est introuvable. Génération en cours...")

        # Génère les documents et sauvegarde aussi un JSON
        documents = document_sparse()
        return documents

    else:
        print(f"[INFO] Fichier SPARSE déjà existant : {SPARSE_JSON_PATH}")
        documents = document_sparse(existing=True)
        return documents
        
def load_data_exact():
    #Si pas de sauvegarde en crée une, sinon la charge
    if not os.path.exists(EXACT_JSON_PATH):
        print(f"[INFO] Le fichier EXACT_JSON est introuvable. Génération en cours...")

        # Génère les documents et sauvegarde un JSON
        documents = document_exact()
        return documents

    else:
        print(f"[INFO] Fichier JSON déjà existant : {EXACT_JSON_PATH}")
        documents = document_exact(existing=True)
        return documents