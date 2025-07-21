import streamlit as st
from core.data_loader import load_data_sparse
from core.sparse_builder import build_sparse_index
from core.sparse_search import search_sparse, get_top_terms_per_document
from preprocess.processed_sparse import preprocess_query
from app.common_ui import display_sparse_results
from config.settings import TOP_K_RESULTS

def run_sparse_app():
    st.title("Moteur de recherche par similarité")

    with st.spinner("Chargement des données..."):
        print("[INFO] Chargement des données sparse...")
        documents = load_data_sparse()  # doit renvoyer les documents avec metadata {"study_id", "section_name"}
        vectorizers, sparse_matrices, section_metadata = build_sparse_index(documents)

        # mapping pour récupérer les documents associés à chaque section
        section_documents = {}
        for section in sparse_matrices:
            docs = [doc for doc in documents if doc.metadata.get("section_name") == section]
            section_documents[section] = docs

    all_sections = sorted({doc.metadata.get("section_name", "UNKNOWN") for doc in documents})
    sections_options = ["Toutes les sections"] + all_sections

    selected_section = st.radio("Choisissez une section", sections_options, horizontal=True)    

    query = st.text_input("Entrez votre requête")

    if query:
        query_cleaned = preprocess_query(query)
        print(f"[INFO] Requête prétraitée : {query_cleaned}")

        results = search_sparse(
            query=query_cleaned,
            vectorizers=vectorizers,
            sparse_matrices=sparse_matrices,
            section_metadata=section_metadata,
            section_documents=section_documents,
            k=TOP_K_RESULTS,
            selected_section=selected_section
        )

        top_terms_by_study = get_top_terms_per_document(
            vectorizers, sparse_matrices, section_metadata
        )

        display_sparse_results(results, query, query_cleaned, top_terms_by_study)
