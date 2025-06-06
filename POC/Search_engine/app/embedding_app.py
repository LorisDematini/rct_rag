# app/embedding_app.py

import json
import streamlit as st
from core.data_loader import load_data_embeddings
from core.vectorizer_embedding import EmbeddingSearchEngine
from preprocess.processed_emb import TextPreprocessor
from config.settings import TOP_K_RESULTS
from config.paths import RAW_JSON_PATH
from app.common_ui import display_embedding_results

def load_embedding_search_engine():
    data = load_data_embeddings()
    return EmbeddingSearchEngine(data)

def run_embedding_app():
    st.title("Moteur de recherche sémantique")
    query = st.text_input("Entrez votre requête", "")
    search_engine = load_embedding_search_engine()

    if query:
        print("[INFO] Prétraitement de la requête...")
        preprocessor = TextPreprocessor()
        preprocessed_query = preprocessor.preprocess(query)
        
        print(f"[INFO] Requête prétraitée : {preprocessed_query}")
        
        results = search_engine.search(preprocessed_query, top_k=TOP_K_RESULTS)
        
        with open(RAW_JSON_PATH, "r", encoding="utf-8") as f:
            summary_data = json.load(f)
        display_embedding_results(results, query, summary_data)
