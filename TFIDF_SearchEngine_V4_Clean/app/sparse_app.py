# sparse_app.py

from core.data_loader import load_data_sparse
from core.sparse_builder import build_sparse_index
from core.sparse_search import search_sparse
from core.top_terms import get_top_terms
from preprocess.processed_sparse import preprocess_query
from display.display_sparse import display_sparse_results
from display.display_utils import spinner_context, title_print, text_input

def run_sparse_app():
    titre = "Moteur de recherche par similarité"
    title_print(titre)

    with spinner_context():
        print("[INFO] Chargement des données sparse...")
        documents = load_data_sparse()
        vectorizer, sparse_matrix, study_ids, full_docs = build_sparse_index(documents)

    query = text_input()

    if query:
        query_cleaned = preprocess_query(query)
        print(f"Requête prétraitée : {query_cleaned}")

        results = search_sparse(query_cleaned, vectorizer, sparse_matrix, study_ids, full_docs)

        top_terms_by_study = get_top_terms(vectorizer, sparse_matrix, study_ids)

        display_sparse_results(results, query, query_cleaned, top_terms_by_study)
