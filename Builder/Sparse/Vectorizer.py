import pickle
import numpy as np
from scipy import sparse
from sklearn.feature_extraction.text import TfidfVectorizer
from Config import VECTOR_PATH, MATRIX_PATH, STUDY_IDS_PATH


def build_save_sparse_index(documents, save=True):
    study_ids = []
    study_sections = {}
    study_texts = []

    for doc in documents:
        study_id = doc.metadata.get("study_id", "ID inconnu")
        section_content = doc.page_content
        if study_id not in study_sections:
            study_sections[study_id] = []
        study_sections[study_id].append(section_content)

    for study_id, sections in study_sections.items():
        full_text = " ".join(sections)
        study_texts.append(full_text.strip())
        study_ids.append(study_id)

    vectorizer = TfidfVectorizer(max_df=0.95)
    sparse_matrix = vectorizer.fit_transform(study_texts)

    
    with open(VECTOR_PATH, "wb") as f:
        pickle.dump(vectorizer, f)

    sparse.save_npz(MATRIX_PATH, sparse_matrix)
    np.save(STUDY_IDS_PATH, np.array(study_ids))

    print(f"Vectorizer saved to: {VECTOR_PATH}")
    print(f"Matrix sparse saved to: {MATRIX_PATH}")
    print(f"List of Study_ids: {STUDY_IDS_PATH}")

    return vectorizer, sparse_matrix, study_ids
