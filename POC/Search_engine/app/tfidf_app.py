import streamlit as st
from core.data_loader import load_data_tfidf
from core.vectorizer_tfidf import TfidfRetriever
from preprocess.processed_tfidf import preprocess_query
from app.common_ui import display_results
from config.settings import TOP_K_RESULTS


def run_tfidf_app():
    st.title("Moteur de recherche TF-IDF")

    # Chargement des données
    with st.spinner("Chargement des données..."):
        print("[INFO] Chargement des données TF-IDF...")
        documents = load_data_tfidf()
        engine = TfidfRetriever(documents)

    # Interface utilisateur
    query = st.text_input("Entrez votre requête")

    if query:
        query_cleaned = preprocess_query(query)  # Prétraitement de la requête
        print(f"Requête prétraitée : {query_cleaned}")  # Affichage de la requête prétraitée
        results = engine.retrieve(query_cleaned, k=TOP_K_RESULTS)  # Recherche avec retrieve()
        display_results(results, query)  # Affichage des résultats