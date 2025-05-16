"""
dense_app.py

Ce module constitue l'interface principale de l'application Streamlit pour le moteur 
de recherche sémantique dense basé sur les embeddings. Il permet à l'utilisateur 
d'entrer une requête, la prétraite, interroge l’index vectoriel, puis affiche les 
résultats pertinents avec leurs sections de contenu.

Fonctions :
- load_dense_search_engine() : Charge les données vectorisées et initialise le moteur de recherche dense.
- run_dense_app() : Gère l'interface utilisateur Streamlit, le traitement de la requête et l'affichage des résultats via `display_dense_results`.
"""


import json
import streamlit as st
from core.data_loader import load_data_dense
from core.vectorizer_dense import DenseSearchEngine
from preprocess.processed_dense import TextPreprocessor
from config.settings import TOP_K_RESULTS
from config.paths import RAW_JSON_PATH, DENSE_JSON_PATH
from app.common_ui import display_dense_results
from core.data_loader import load_dense_sections

def load_dense_search_engine():
    data = load_data_dense()
    return DenseSearchEngine(data)

def run_dense_app():
    st.title("Moteur de recherche Dense")
    query = st.text_input("Entrez votre requête", "")
    search_engine = load_dense_search_engine()

    if query:
        print("[INFO] Prétraitement de la requête...")
        preprocessor = TextPreprocessor()
        preprocessed_query = preprocessor.preprocess(query)
        
        print(f"[INFO] Requête prétraitée : {preprocessed_query}")
        
        results = search_engine.search(preprocessed_query, top_k=TOP_K_RESULTS)
        
        study_sections = load_dense_sections(DENSE_JSON_PATH)

        display_dense_results(results, query, study_sections)
