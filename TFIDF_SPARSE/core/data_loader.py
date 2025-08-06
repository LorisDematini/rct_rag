import pickle
import numpy as np
from scipy import sparse
import json
from config import VECTOR_PATH, MATRIX_PATH, STUDY_IDS_PATH, SPARSE_PCKL_PATH, TOP_TERMS_PATH

def load_file_pkl(file_path: str):
    """Load a pickle file."""
    with open(file_path, 'rb') as file:
        return pickle.load(file)

def load_file_json(file_path: str):
    """Load a JSON file."""
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)

def load_sparse():
    """
    Load all necessary components for the sparse (TF-IDF) search engine.

    Returns:
        vectorizer: The trained TfidfVectorizer.
        sparse_matrix: The TF-IDF document-term matrix.
        study_ids: List of study IDs corresponding to matrix rows.
        documents: List of LangChain Document objects.
        top_terms: Top representative words per document (dict).
    """
    top_terms = load_file_json(TOP_TERMS_PATH)
    documents = load_file_pkl(SPARSE_PCKL_PATH)
    vectorizer = load_file_pkl(VECTOR_PATH)
    sparse_matrix = sparse.load_npz(MATRIX_PATH)
    study_ids = np.load(STUDY_IDS_PATH).tolist()

    return vectorizer, sparse_matrix, study_ids, documents, top_terms
