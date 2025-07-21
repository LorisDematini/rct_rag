# sparse_search.py

from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from config.settings import TOP_K_RESULTS

def search_sparse(query: str, vectorizer, sparse_matrix, study_ids, documents, k=TOP_K_RESULTS):
    query_vec = vectorizer.transform([query])
    similarities = cosine_similarity(query_vec, sparse_matrix).flatten()
    sorted_indices = np.argsort(similarities)[::-1]

    results = []
    for idx in sorted_indices[:k]:
        if similarities[idx] > 0:
            results.append({
                "study_id": study_ids[idx],
                "score": similarities[idx],
                "document": documents[idx]
            })
    return results
