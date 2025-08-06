# sparse_search.py

from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from typing import List, Dict, Any

def search_sparse(query: str, vectorizer, sparse_matrix, study_ids: List[str], documents: List[str], k: int = 40) -> List[Dict[str, Any]]:
    """
    Perform a sparse (TF-IDF) search over a collection of documents.

    Args:
        query (str): The user's textual search query.
        vectorizer: The trained TF-IDF vectorizer.
        sparse_matrix: The sparse TF-IDF matrix representing all documents.
        study_ids (List[str]): A list of study IDs corresponding to the documents.
        documents (List[str]): A list of document contents.
        k (int, optional): The number of top relevant results to return (default is 40).

    Returns:
        List[Dict[str, Any]]: A list of results, each containing:
            - 'study_id': ID of the matching study.
            - 'score': Cosine similarity score with the query.
            - 'document': Content of the matched document.
    """
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
