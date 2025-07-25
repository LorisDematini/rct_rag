'''
paths.py

Ce module définit les chemins vers tous les fichiers de données.

- Racine : `BASE_DIR` et `DATA_DIR` pointent vers la structure de base du projet.

- PDF_FOLDER : dossier contenant les fichiers sources.

- Fichiers JSON :
    - `SECTIONS_JSON_PATH` : Sections choisis pour le moteur SPARSE (limité)
    - `SECTIONS_FULL_JSON_PATH` : Sections choisis pour le moteur EXACTE (TOUT)
    - `SUMMARY_JSON_PATH` : documents bruts en JSON.
    - `SPARSE_JSON_PATH`, `EXACT_JSON_PATH` : versions prétraitées pour les moteurs de recherche sparse et exact.

- Acronymes :
    - `ACRONYMS_FILE` : Acronymes extraits des tableaux et ACR = def(ACR)
    - `ACRONYMS_FILE_UNIQUE` :  Liste d'acronymes uniques.

- Fichiers de sauvegarde générés pour la recherche sparse :
    - `TOP_TERMS_PATH` : termes TF-IDF les plus représentatifs par document.
    - `VECTOR_PATH`, `MATRIX_PATH`, `STUDY_IDS_PATH` : vectoriseur TF-IDF, matrice sparse et identifiants de documents.

Ce module centralise les chemins pour éviter les chemins ailleurs dans le projet.
'''

import os

# Racine du projet
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")

#Dossier contenant les fichiers d'origine docx
PDF_FOLDER = os.path.join(DATA_DIR, "pdf")

#Fichiers d'entrées contenant les données du texte
SECTIONS_JSON_PATH = os.path.join(DATA_DIR, "sections_sorted.json")
SECTIONS_FULL_JSON_PATH = os.path.join(DATA_DIR, "sections_sorted_full.json")
SUMMARY_JSON_PATH = os.path.join(DATA_DIR, "summary.json")

#Fichiers contenant les acronymes du texte
ACRONYMS_FILE = os.path.join(DATA_DIR, "extracted_acronym_final.json")
ACRONYMS_FILE_UNIQUE = os.path.join(DATA_DIR, "unique_acronym.json")

# Fichier de sortie prétraité spécifique aux moteurs
SPARSE_JSON_PATH = os.path.join(DATA_DIR, "summarySparse_pre.json")
EXACT_JSON_PATH = os.path.join(DATA_DIR, "summaryExact_pre.json")

#Fichiers de sauvegarde 
TOP_TERMS_PATH = os.path.join(DATA_DIR, "top_terms_sparse.json")
VECTOR_PATH = os.path.join(DATA_DIR, "tfidf_vectorizer.pkl")
MATRIX_PATH = os.path.join(DATA_DIR, "sparse_matrix.npz")
STUDY_IDS_PATH = os.path.join(DATA_DIR, "study_ids.npy")