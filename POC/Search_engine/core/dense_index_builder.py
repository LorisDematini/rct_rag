"""
dense_index_builder.py

Ce module implémente la classe `DenseIndexBuilder`, un outil de création et de gestion d’un index vectoriel FAISS
basé sur des embeddings sémantiques (modèle HuggingFace) pour la recherche d’informations.

Fonctionnalités :
- Prétraite les documents avec un pipeline de nettoyage personnalisé.
- Sauvegarde les documents prétraités dans un fichier JSON local.
- Crée un index vectoriel FAISS à partir des embeddings générés.
- Charge un index existant depuis le disque ou en crée un nouveau à partir de données brutes.

Classe :
- DenseIndexBuilder :
    - __init__() : initialise le modèle d’embedding et le préprocesseur de texte.
    - preprocess_documents(documents) : applique un nettoyage et un filtrage sur les documents fournis.
    - save_preprocessed_documents_to_json(documents) : sauvegarde les documents nettoyés en JSON.
    - create_faiss_index(documents) : construit et sauvegarde un index FAISS à partir des documents.
    - load_or_build_index(raw_data=None) : charge un index existant ou le construit à partir des données RAW.

Utilisé pour la recherche dense dans l’application Streamlit.
"""

import os
import json
from langchain_community.vectorstores import FAISS
from langchain.schema import Document
from langchain_huggingface import HuggingFaceEmbeddings
from collections import defaultdict

from preprocess.processed_dense import TextPreprocessor
from config.paths import DENSE_JSON_PATH, FAISS_INDEX_PATH
from config.settings import EMBEDDING_MODEL_NAME

class DenseIndexBuilder:
    def __init__(self):
        self.embedding_model = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL_NAME)
        self.preprocessor = TextPreprocessor()

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

    def save_preprocessed_documents_to_json(self, documents):
        doc_dump = [{
            "page_content": doc.page_content,
            "metadata": doc.metadata
        } for doc in documents]

        with open(DENSE_JSON_PATH, "w", encoding="utf-8") as f:
            json.dump(doc_dump, f, ensure_ascii=False, indent=4)
        print(f"[DEBUG] Sauvegarde des documents dans {DENSE_JSON_PATH}")

    def create_faiss_index(self, documents):
        print(f"[DEBUG] Création de l'index FAISS avec {len(documents)} documents")
        vector_store = FAISS.from_documents(documents, self.embedding_model)
        vector_store.save_local(FAISS_INDEX_PATH)
        print(f"[INFO] Index FAISS sauvegardé dans {FAISS_INDEX_PATH}")
        return vector_store

    def load_or_build_index(self, raw_data=None):
        if os.path.exists(FAISS_INDEX_PATH):
            print(f"[INFO] Index FAISS trouvé à {FAISS_INDEX_PATH}")
            return FAISS.load_local(
                FAISS_INDEX_PATH,
                self.embedding_model,
                allow_dangerous_deserialization=True
            )

        if os.path.exists(DENSE_JSON_PATH):
            print(f"[INFO] Chargement des documents depuis {DENSE_JSON_PATH}")
            with open(DENSE_JSON_PATH, "r", encoding="utf-8") as f:
                json_docs = json.load(f)
            documents = [
                Document(page_content=d["page_content"], metadata=d["metadata"])
                for d in json_docs
            ]
        else:
            if raw_data is None:
                raise ValueError("[ERREUR] Aucune donnée RAW fournie pour construire l’index.")
            documents = self.preprocess_documents(raw_data)
            self.save_preprocessed_documents_to_json(documents)

        vector_store = self.create_faiss_index(documents)
        return vector_store
