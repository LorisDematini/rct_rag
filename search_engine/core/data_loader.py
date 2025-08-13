import pickle
import numpy as np
from scipy import sparse
import json
from config import (
    VECTOR_PATH,
    MATRIX_PATH,
    STUDY_IDS_PATH,
    SPARSE_PCKL_PATH,
    TOP_TERMS_PATH,
    EXACT_PCKL_PATH,
    AVAILABLE_SECTIONS_JSON_PATH,
    SUMMARY_JSON_PATH
)

def load_file_pkl(file_path: str):
    """
    Load a Python object from a Pickle file.

    Args:
        file_path (str): Path to the .pkl file.

    Returns:
        Any: The object loaded from the pickle file.
    """
    with open(file_path, 'rb') as file:
        return pickle.load(file)


def load_file_json(file_path: str):
    """
    Load data from a JSON file.

    Args:
        file_path (str): Path to the JSON file.

    Returns:
        Any: Parsed JSON content (usually a dict or list).
    """
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


def load_sparse():
    """
    Load all components required for the sparse (TF-IDF-based) search engine.

    Returns:
        tuple:
            - vectorizer (TfidfVectorizer): Trained TF-IDF vectorizer.
            - sparse_matrix (scipy.sparse.csr_matrix): TF-IDF document-term matrix.
            - study_ids (list): List of study IDs corresponding to matrix rows.
            - documents (list): List of LangChain Document objects.
            - top_terms (dict): Most representative terms for each study/document.
    """
    top_terms = load_file_json(TOP_TERMS_PATH)
    documents = load_file_pkl(SPARSE_PCKL_PATH)
    vectorizer = load_file_pkl(VECTOR_PATH)
    sparse_matrix = sparse.load_npz(MATRIX_PATH)
    study_ids = np.load(STUDY_IDS_PATH).tolist()

    return vectorizer, sparse_matrix, study_ids, documents, top_terms


def load_exact():
    """
    Load all components required for the exact keyword search engine.

    Returns:
        tuple:
            - documents_exact (list): List of LangChain Document objects (one per section).
            - list_sections (list): Alphabetically sorted list of all available section names.
    """
    documents_exact = load_file_pkl(EXACT_PCKL_PATH)
    list_sections = load_file_json(AVAILABLE_SECTIONS_JSON_PATH)

    return documents_exact, list_sections


def load_list():
    """
    Load the component required for the database viewer.

    Returns:
        - summary (Dict) Study_id : content
    """

    summary = load_file_json(SUMMARY_JSON_PATH)

    return summary