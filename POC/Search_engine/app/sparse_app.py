"""
sparse_app.py

Ce module gère l’interface Streamlit pour le moteur de recherche sparse.
Il permet à l’utilisateur d’entrer une requête, la prétraite, lance une recherche par mots-clés 
dans l’ensemble des documents, puis affiche les résultats de manière lisible.

Fonctions :
- run_sparse_app() : Fonction principale qui initialise l’interface utilisateur, 
  traite la requête via TF-IDF, et affiche les résultats avec `display_sparse_results`.
"""

import streamlit as st
from core.data_loader import load_data_sparse
from core.vectorizer_sparse import SparseRetriever
from preprocess.processed_sparse import preprocess_query
from app.common_ui import display_sparse_results
from config.settings import TOP_K_RESULTS


def run_sparse_app():
    st.title("Moteur de recherche sparse")

    # Chargement des données
    with st.spinner("Chargement des données..."):
        print("[INFO] Chargement des données sparse...")
        documents = load_data_sparse()
        engine = SparseRetriever(documents)

    # Interface utilisateur
    query = st.text_input("Entrez votre requête")

    if query:
        query_cleaned = preprocess_query(query)
        print(f"Requête prétraitée : {query_cleaned}")
        results = engine.retrieve(query_cleaned, k=TOP_K_RESULTS)
        display_sparse_results(results, query)