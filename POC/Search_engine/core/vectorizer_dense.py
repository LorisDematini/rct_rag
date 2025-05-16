"""
vectorizer_dense.py

Ce module définit la classe `DenseSearchEngine` pour effectuer une recherche sémantique
(dense) à l'aide de FAISS et d'un modèle d'embedding HuggingFace.

Fonctionnalités principales :
- Initialisation du moteur avec chargement ou création d’un index FAISS basé sur les embeddings.
- Prétraitement des documents avec un `TextPreprocessor` (normalisation, nettoyage, etc.).
- Sauvegarde locale des documents prétraités au format JSON.
- Recherche par similarité avec filtre sur les `top_k` études distinctes les plus pertinentes.

Classes :
- DenseSearchEngine :
    - __init__(self, data=None) : initialise ou charge l’index FAISS.
    - preprocess_documents(documents) : applique le nettoyage NLP aux documents.
    - create_faiss_index(documents) : génère l’index FAISS à partir de documents prétraités.
    - search(query, top_k) : renvoie les `top_k` meilleures études selon la similarité cosine.
    - save_preprocessed_documents_to_json(documents) : sauvegarde les documents indexés.

"""

import os
import json
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from preprocess.processed_dense import TextPreprocessor
from config.paths import DENSE_JSON_PATH, FAISS_INDEX_PATH
from config.settings import EMBEDDING_MODEL_NAME
from langchain.schema import Document
from collections import defaultdict

class DenseSearchEngine:
    def __init__(self, data=None):
        # Utilisation de HuggingFaceEmbeddings pour transformer les textes en vecteurs
        self.dense_model = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL_NAME)
        # Préparer le préprocesseur
        self.preprocessor = TextPreprocessor()

        if os.path.exists(FAISS_INDEX_PATH):
            # Si l'index FAISS existe déjà, on le charge
            self.vector_store = FAISS.load_local(FAISS_INDEX_PATH, self.dense_model, allow_dangerous_deserialization=True)
        else:
            # Si l'index FAISS n'existe pas, on le crée à partir des données
            if data is None:
                raise ValueError("Les données sont nécessaires pour créer l'index FAISS.")
            preprocessed_data = self.preprocess_documents(data)
            self.vector_store = self.create_faiss_index(preprocessed_data)
            print(f"[INFO] Index FAISS créé et sauvegardé dans '{FAISS_INDEX_PATH}'.")
            self.vector_store.save_local(FAISS_INDEX_PATH)
            # Sauvegarder les documents prétraités dans un fichier JSON
            # self.save_raw_documents_for_debug(preprocessed_data)
            self.save_preprocessed_documents_to_json(preprocessed_data)

    def preprocess_documents(self, documents):
        preprocessed_documents = []
        print(f"[DEBUG] Documents avant prétraitement: {len(documents)}")
        for doc in documents:
            preprocessed_text = self.preprocessor.preprocess(doc.page_content)
            if preprocessed_text.strip():
                preprocessed_documents.append(
                    Document(page_content=preprocessed_text, metadata=doc.metadata)
                )
        print(f"[DEBUG] Documents après prétraitement: {len(preprocessed_documents)}")
        return preprocessed_documents

    def create_faiss_index(self, documents):
        print(f"[DEBUG] Nombre de documents envoyés à FAISS: {len(documents)}")
        return FAISS.from_documents(documents, self.dense_model)

    def search(self, query, top_k):
        preprocessed_query = self.preprocessor.preprocess(query)

        print(f"[DEBUG] Requête prétraitée après transformation : {preprocessed_query}")

        raw_results = self.vector_store.similarity_search_with_score(preprocessed_query, k=100)

        # Filtrage pour top_k études
        unique_titles = set()
        filtered_results = []
        for doc, score in raw_results:
            title = doc.metadata.get("study_id", "")
            if title not in unique_titles:
                unique_titles.add(title)
                filtered_results.append((doc, score))
            if len(filtered_results) >= top_k:
                break

        scored_sections_by_study = defaultdict(list)
        for doc, score in filtered_results:
            title = doc.metadata.get("study_id", "UNKNOWN")
            similarity = 1 / (1 + score)

            scored_sections_by_study[title].append({
                "text": doc.page_content,
                "score": similarity,
                "raw_score": score
            })
        return scored_sections_by_study
    
    def save_preprocessed_documents_to_json(self, documents):
        doc_dump = []
        for doc in documents:
            doc_dump.append({
                "page_content": doc.page_content,
                "metadata": doc.metadata
            })
        with open(DENSE_JSON_PATH, "w", encoding="utf-8") as f:
            json.dump(doc_dump, f, ensure_ascii=False, indent=4)
        print(f"[DEBUG] Sauvegarde des documents d'index dans {DENSE_JSON_PATH}")