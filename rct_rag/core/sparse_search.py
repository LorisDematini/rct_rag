"""
sparse_search.py

Module de recherche sémantique utilisant la similarité cosinus sur une représentation TF-IDF.

Fonction principale :
- search_sparse(query, vectorizer, sparse_matrix, study_ids, documents, k) :
    Calcule la similarité cosinus entre la requête vectorisée et la matrice TF-IDF des documents,
    puis retourne les `k` documents les plus similaires avec leur score et métadonnées associées.
"""

from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from config.settings import TOP_K_RESULTS

#Utilisation du vectorizer pour transformer la requête et faire une similarité cosine
def search_sparse(query: str, vectorizer, sparse_matrix, study_ids, documents, k=TOP_K_RESULTS):
    query_vec = vectorizer.transform([query])
    #requête : [1,N], sparse_matrix : [D,N]; similarities : [1,D] où D est le nombre de documents
    similarities = cosine_similarity(query_vec, sparse_matrix).flatten()
    #On trie par ordre décroissant
    sorted_indices = np.argsort(similarities)[::-1]

    results = []
    for idx in sorted_indices[:k]:
        if similarities[idx] > 0:
            #Liste de dictionnaire pour le display
            results.append({
                "study_id": study_ids[idx],
                "score": similarities[idx],
                "document": documents[idx]
            })
    return results
