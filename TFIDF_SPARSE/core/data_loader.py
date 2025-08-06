import pickle
import numpy as np
from scipy import sparse
import json
from config.paths import VECTOR_PATH, MATRIX_PATH, STUDY_IDS_PATH, SPARSE_PCKL_PATH, TOP_TERMS_PATH

def load_top_terms():
    with open(TOP_TERMS_PATH, "r", encoding="utf-8") as file_top_terms:
        return json.load(file_top_terms)
    
def load_data_sparse():
    with open(SPARSE_PCKL_PATH, 'rb') as f:
        documents = pickle.load(f)
    return documents

def load_sparse_index():
    with open(VECTOR_PATH, "rb") as f:
        vectorizer = pickle.load(f)

    sparse_matrix = sparse.load_npz(MATRIX_PATH)
    study_ids = np.load(STUDY_IDS_PATH).tolist()

    return vectorizer, sparse_matrix, study_ids
