from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from config.settings import TOP_K_MOTS

def search_sparse(query, vectorizers, sparse_matrices, section_metadata, section_documents, k=10, selected_section="Toutes les sections"):

    all_results = []

    sections = (
        [selected_section] if selected_section != "Toutes les sections"
        else vectorizers.keys()
    )

    for section in sections:
        vectorizer = vectorizers.get(section)
        matrix = sparse_matrices.get(section)
        metadata_list = section_metadata.get(section)
        docs = section_documents.get(section)

        if vectorizer is None or matrix is None:
            continue

        query_vec = vectorizer.transform([query])
        similarities = cosine_similarity(query_vec, matrix).flatten()
        sorted_indices = np.argsort(similarities)[::-1]

        for idx in sorted_indices[:k]:
            score = similarities[idx]
            if score > 0:
                md = metadata_list[idx]
                all_results.append({
                    "study_id": md.get("study_id"),
                    "section_name": section,
                    "score": score,
                    "document": docs[idx]
                })

    # trier tous les résultats ensemble, quel que soit la section
    all_results.sort(key=lambda x: x["score"], reverse=True)

    return all_results[:k]

def get_top_terms_per_document(vectorizers, sparse_matrices, section_metadata, top_n=TOP_K_MOTS):
    results = {}

    for section, vectorizer in vectorizers.items():
        feature_names = vectorizer.get_feature_names_out()
        matrix = sparse_matrices[section]
        study_ids = [md["study_id"] for md in section_metadata[section]]

        for i, row in enumerate(matrix):
            row_dense = row.toarray().flatten()
            top_indices = row_dense.argsort()[::-1][:top_n]
            top_terms = [
                (feature_names[idx], row_dense[idx])
                for idx in top_indices if row_dense[idx] > 0
            ]
            results[(study_ids[i], section)] = top_terms

    return results
