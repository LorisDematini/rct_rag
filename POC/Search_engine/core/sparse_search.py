"""
sparse_search.py

Ce module implémente le moteur de recherche sparse basé sur la similarité cosinus 
entre un vecteur de requête TF-IDF et une matrice d’études vectorisées.

Classe :
- SparseSearchEngine : Prend un index TF-IDF (construit via `SparseBuilder`), transforme une requête,
  calcule les similarités cosinus et retourne les études les plus pertinentes.

Attributs :
- vectorizer : Le TfidfVectorizer entraîné sur les textes concaténés des études.
- sparse_matrix : Matrice TF-IDF (une ligne par étude).
- study_ids : Liste des identifiants d’études, dans le même ordre que la matrice.
- documents : Liste des objets Document d'origine.

Méthodes :
- search(query, k=10) : Retourne les `k` études les plus similaires à la requête, 
  sous forme de dictionnaires contenant `study_id`, `score`, et `document`.
"""


from typing import List
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

class SparseSearchEngine:
    def __init__(self, index):
        self.vectorizer = index.vectorizer
        self.sparse_matrix = index.sparse_matrix
        self.study_ids = index.study_ids
        self.documents = index.documents


    def search(self, query: str, k: int = 10) -> List[dict]:
        query_vec = self.vectorizer.transform([query])
        similarities = cosine_similarity(query_vec, self.sparse_matrix).flatten()
        sorted_indices = np.argsort(similarities)[::-1]
        results = []

        for idx in sorted_indices[:k]:
            if similarities[idx] > 0:
                results.append({
                    "study_id": self.study_ids[idx],
                    "score": similarities[idx],
                    "document": self.documents[idx]
                })

        return results
