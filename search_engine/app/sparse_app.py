"""
sparse_app.py

This module runs the Streamlit application for similarity-based search using TF-IDF.

Main function: `run_sparse_app()`

Main steps:
1. Displays the title "Similarity Search Engine".
2. Loads preprocessed documents using `load_sparse()`.
3. Builds the TF-IDF index (returns the vectorizer, sparse matrix, study_ids, and documents).
4. Retrieves the user query and preprocesses it via `preprocess_query()`.
5. Performs cosine similarity search using `search_sparse()`.
6. Retrieves top terms per study via `load_sparse()` output.
7. Displays search results and top terms using `display_sparse_results()`.

This engine enables semantic search using TF-IDF weighting to find the most relevant sections to a user's query.
"""

from core import load_sparse, search_sparse
from display import display_sparse_results, title_print, text_input
from config import title_sparse

def run_sparse_app():
    """
    Runs the Streamlit sparse search app.

    Inputs:
    - User query entered via Streamlit text input.

    Outputs:
    - Streamlit interface displaying ranked results and relevant terms per study.
    """

    # Display the app title
    title_print(title_sparse)

    # Returns TfidfVectorizer, document-term matrix, list of study IDs, LangChain Documents, top TF-IDF terms
    vectorizer, sparse_matrix, study_ids, documents, top_terms = load_sparse()
        
    # Get user query input from the UI
    query_sparse = text_input()

    if query_sparse:
        # Perform cosine similarity search between query and TF-IDF index
        # Returns a list of matched sections with similarity scores and metadata
        results, query_cleaned = search_sparse(query_sparse, vectorizer, sparse_matrix, study_ids, documents)

        # Display the ranked results and top terms per study using results and Streamlit
        display_sparse_results(results, query_sparse, query_cleaned, top_terms)