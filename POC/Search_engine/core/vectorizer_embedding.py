from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from preprocess.processed_emb import TextPreprocessor
import os
import json
from config.paths import EMB_JSON_PATH, FAISS_INDEX_PATH, DOC_DUMP_PATH
from langchain.schema import Document
from collections import defaultdict

class EmbeddingSearchEngine:
    def __init__(self, data=None):
        # Utilisation de HuggingFaceEmbeddings pour transformer les textes en vecteurs
        self.embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")
        
        # Préparer le préprocesseur
        self.preprocessor = TextPreprocessor()
        
        if os.path.exists(FAISS_INDEX_PATH):
            # Si l'index FAISS existe déjà, on le charge
            self.vector_store = FAISS.load_local(FAISS_INDEX_PATH, self.embedding_model, allow_dangerous_deserialization=True)
        else:
            # Si l'index FAISS n'existe pas, on le crée à partir des données
            if data is None:
                raise ValueError("Les données sont nécessaires pour créer l'index FAISS.")
            preprocessed_data = self.preprocess_documents(data)
            self.vector_store = self.create_faiss_index(preprocessed_data)
            print(f"[INFO] Index FAISS créé et sauvegardé dans '{FAISS_INDEX_PATH}'.")
            self.vector_store.save_local(FAISS_INDEX_PATH)
            # Sauvegarder les documents prétraités dans un fichier JSON
            self.save_raw_documents_for_debug(preprocessed_data)
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
        return FAISS.from_documents(documents, self.embedding_model)

    
    def save_raw_documents_for_debug(self, documents):
        doc_dump = []
        for doc in documents:
            doc_dump.append({
                "page_content": doc.page_content,
                "metadata": doc.metadata
            })
        with open(DOC_DUMP_PATH, "w", encoding="utf-8") as f:
            json.dump(doc_dump, f, ensure_ascii=False, indent=4)
        print(f"[DEBUG] Sauvegarde des documents d'index dans {DOC_DUMP_PATH}")


    def search(self, query, top_k):
        preprocessed_query = self.preprocessor.preprocess(query)

        if isinstance(preprocessed_query, list):
            preprocessed_query = " ".join(preprocessed_query)

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
        """Sauvegarder les documents prétraités dans un fichier JSON"""
        preprocessed_data = {}
        for doc in documents:
            study_id = doc.metadata.get("study_id", "unknown_study_id")
            if study_id not in preprocessed_data:
                preprocessed_data[study_id] = []
            preprocessed_data[study_id].append(doc.page_content)
        
        with open(EMB_JSON_PATH, "w", encoding="utf-8") as f:
            json.dump(preprocessed_data, f, ensure_ascii=False, indent=4)
        print(f"[INFO] Documents prétraités sauvegardés dans '{EMB_JSON_PATH}'.")
