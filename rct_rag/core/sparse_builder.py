"""
sparse_builder.py

Ce module construit, sauvegarde et recharge l'index TF-IDF sparse pour la recherche sémantique.

Fonctions principales :
- save_sparse_index(documents, save=True) :
    Regroupe les textes par protocole, crée la matrice TF-IDF, sauvegarde les artefacts
    (vectorizer, matrice sparse, liste des study_ids) sur disque, et retourne ces objets.

- build_sparse_index(documents) :
    Recharge l'index TF-IDF depuis les fichiers sauvegardés s'ils existent,
    sinon reconstruit et sauvegarde l'index à partir des documents fournis.
"""


import os
import pickle
import numpy as np
from scipy import sparse
from sklearn.feature_extraction.text import TfidfVectorizer
from config.paths import VECTOR_PATH, MATRIX_PATH, STUDY_IDS_PATH

#Sauvegarde des différents éléments si c'est pas déjà fait
def save_sparse_index(documents, save=True):
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

    if save:
        with open(VECTOR_PATH, "wb") as f:
            pickle.dump(vectorizer, f)

        sparse.save_npz(MATRIX_PATH, sparse_matrix)
        np.save(STUDY_IDS_PATH, np.array(study_ids))

    return vectorizer, sparse_matrix, study_ids, documents


#Vérifie qu'on a tout, sinon les enregistre et les télécharge
def build_sparse_index(documents):
    if not (os.path.exists(VECTOR_PATH) and os.path.exists(MATRIX_PATH) and os.path.exists(STUDY_IDS_PATH)):
        print("[INFO] Sparse index non trouvé, reconstruction...")
        return save_sparse_index(documents, save=True)

    with open(VECTOR_PATH, "rb") as f:
        vectorizer = pickle.load(f)

    sparse_matrix = sparse.load_npz(MATRIX_PATH)
    study_ids = np.load(STUDY_IDS_PATH).tolist()

    return vectorizer, sparse_matrix, study_ids, documents
