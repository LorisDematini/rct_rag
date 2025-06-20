"""
paths.py

Ce module centralise tous les chemins utilisés dans le projet pour accéder aux fichiers de données.
Il permet de garantir une organisation claire et évite la duplication de chemins en dur dans le code.

Variables définies :
- BASE_DIR : Chemin racine du projet.
- DATA_DIR : Dossier contenant les fichiers de données (`data/`).

Fichiers JSON utilisés :
- RAW_JSON_PATH : Données brutes (`summary.json`) utilisées notamment pour le moteur sparse.
- ACRONYMS_FILE : Dictionnaire d’acronymes et de leurs définitions.
- SPARSE_JSON_PATH : Résultat du prétraitement pour le moteur TF-IDF.
- DENSE_JSON_PATH : Résultat du prétraitement pour le moteur sémantique.
- FAISS_INDEX_PATH : Répertoire contenant l’index FAISS binaire.
"""

import os

# Racine du projet
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")

#Dossier contenant les fichiers d'origine docx
PDF_FOLDER = os.path.join(DATA_DIR, "pdf")

# Répertoire contenant les fichiers de données
SECTIONS_JSON_PATH = os.path.join(DATA_DIR, "sections_sorted.json")
ACRONYMS_FILE = os.path.join(DATA_DIR, "extracted_acronym_final.json")  # Fichier contenant les acronymes et leurs définitions

# Fichier de sortie prétraité spécifique au moteur sparse
SPARSE_JSON_PATH = os.path.join(DATA_DIR, "summarySparse_pre.json")

#OLD RAW
# RAW_JSON_PATH = os.path.join(DATA_DIR, "summary.json")  # Nom du fichier JSON contenant les documents RAW