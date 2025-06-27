import streamlit as st
from core.data_loader import load_data_exact
from core.exact_builder import ExactIndex
from core.exact_search import ExactSearchEngine
from preprocess.processed_sparse import preprocess_query
from app.common_ui import display_exacte_results

def run_exacte_app():
    st.title("Moteur de recherche par mot-clé")

    with st.spinner("Chargement des données..."):
        documents = load_data_exact()
        index = ExactIndex(documents)
        engine = ExactSearchEngine(index)

    all_sections = sorted({doc.metadata.get("section_name", "UNKNOWN") for doc in documents})
    sections_options = ["Toutes les sections"] + all_sections

    selected_section = st.radio("Choisissez une section", sections_options, horizontal=True)

    query = st.text_input("Entrez votre requête")

    if query:
        query_cleaned = preprocess_query(query)
        print(query_cleaned)

        if selected_section == "Toutes les sections":
            selected_sections = None
        else:
            selected_sections = [selected_section]

        results = engine.search(query_cleaned, selected_sections=selected_sections)
        display_exacte_results(results, query, selected_section)
