"""
dense_search_engine.py

Ce module implémente la classe `DenseSearchEngine`, un moteur de recherche sémantique basé sur FAISS 
et des embeddings générés avec un modèle HuggingFace.

Fonctionnalités :
- Charge un index FAISS localement pour effectuer des recherches vectorielles.
- Prétraite la requête utilisateur avant vectorisation.
- Recherche les `k` études les plus pertinentes selon la similarité cosinus (convertie en score).

Classe :
- DenseSearchEngine :
    - __init__() : charge le modèle d’embedding et l’index FAISS existant.
    - search(query, top_k) : retourne les `top_k` études distinctes les plus proches de la requête,
      accompagnées de leurs sections les plus pertinentes et de leurs scores.

Utilisé pour la recherche dense dans l’application Streamlit.
"""


import os
from collections import defaultdict
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

from preprocess.processed_dense import TextPreprocessor
from config.paths import FAISS_INDEX_PATH
from config.settings import EMBEDDING_MODEL_NAME

class DenseSearchEngine:
    def __init__(self):
        self.embedding_model = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL_NAME)
        self.preprocessor = TextPreprocessor()

        if not os.path.exists(FAISS_INDEX_PATH):
            raise FileNotFoundError(
                f"[ERREUR] Index FAISS introuvable à '{FAISS_INDEX_PATH}'. "
            )

        self.vector_store = FAISS.load_local(
            FAISS_INDEX_PATH,
            self.embedding_model,
            allow_dangerous_deserialization=True
        )
        print(f"[INFO] Index FAISS chargé depuis {FAISS_INDEX_PATH}")

    def search(self, query, top_k):
        preprocessed_query = self.preprocessor.preprocess(query)
        print(f"[DEBUG] Requête après prétraitement : {preprocessed_query}")

        raw_results = self.vector_store.similarity_search_with_score(preprocessed_query, k=100)

        unique_titles = set()
        filtered_results = []
        for doc, score in raw_results:
            study_id = doc.metadata.get("study_id", "")
            if study_id not in unique_titles:
                unique_titles.add(study_id)
                filtered_results.append((doc, score))
            if len(filtered_results) >= top_k:
                break

        scored_sections_by_study = defaultdict(list)
        for doc, score in filtered_results:
            study_id = doc.metadata.get("study_id", "UNKNOWN")
            similarity = 1 / (1 + score)

            scored_sections_by_study[study_id].append({
                "text": doc.page_content,
                "score": similarity,
                "raw_score": score
            })

        return scored_sections_by_study
