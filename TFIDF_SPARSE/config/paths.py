'''
paths.py

Ce module définit les chemins vers tous les fichiers et dossiers utilisés dans le projet.

Organisation des chemins :
- Racine : `BASE_DIR` et `DATA_DIR` pointent vers la structure de base du projet.
- Fichiers PDF : dossier contenant les fichiers sources (`PDF_FOLDER`).
- Fichiers JSON :
    - `SECTIONS_JSON_PATH`, `SECTIONS_FULL_JSON_PATH` : sections extraites et nettoyées des documents.
    - `SUMMARY_JSON_PATH` : résumé des documents bruts.
    - `SPARSE_JSON_PATH`, `EXACT_JSON_PATH` : versions prétraitées pour les moteurs de recherche sémantique (sparse) et exact.
- Acronymes :
    - `ACRONYMS_FILE`, `ACRONYMS_FILE_UNIQUE` : acronymes extraits et version dédupliquée.
- Fichiers générés pour la recherche sparse :
    - `TOP_TERMS_PATH` : termes TF-IDF les plus représentatifs par document.
    - `VECTOR_PATH`, `MATRIX_PATH`, `STUDY_IDS_PATH` : vectoriseur TF-IDF, matrice sparse et identifiants de documents.

Ce module centralise les chemins pour éviter les chemins en dur ailleurs dans le projet.
'''

import os

# Racine du projet
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PARENT_OF_BASE = os.path.dirname(BASE_DIR)
BUILDER = os.path.join(PARENT_OF_BASE, "Builder")
DATA_DIR = os.path.join(BUILDER, "Data")

# #Fichiers d'entrées contenant les données du texte
# SECTIONS_FULL_JSON_PATH = os.path.join(DATA_DIR, "sections_sorted_full.json")

#V2
#Dossier contenant les fichiers d'origine docx
PDF_FOLDER = os.path.join(DATA_DIR, "pdf")

SUMMARY_JSON_PATH = os.path.join(DATA_DIR, "summary.json")

#Fichiers contenant les acronymes du texte
ACRONYMS_FILE = os.path.join(DATA_DIR, "extracted_acronym_final.json")
ACRONYMS_FILE_UNIQUE = os.path.join(DATA_DIR, "unique_acronym.json")


SECTIONS_JSON_PATH = os.path.join(DATA_DIR, "sections_sorted.json")


SPARSE_PCKL_PATH = os.path.join(DATA_DIR, "document_sparse.pkl")

VECTOR_PATH = os.path.join(DATA_DIR, "vectorizer.pkl")
MATRIX_PATH = os.path.join(DATA_DIR, "sparse_matrix.npz")
STUDY_IDS_PATH = os.path.join(DATA_DIR, "study_ids.npy")

TOP_TERMS_PATH = os.path.join(DATA_DIR, "TopTermsByStudy.json")