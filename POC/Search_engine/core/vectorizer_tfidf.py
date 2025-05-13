from typing import List
from langchain.schema import Document
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

class TfidfRetriever:
    def __init__(self, documents: List[Document], max_df: float = 0.95):
        self.documents = documents
        # Fusionner le contenu des sections pour chaque étude
        self.study_texts = self.merge_study_sections(documents)
        self.vectorizer = TfidfVectorizer(max_df=max_df)
        self.tfidf_matrix = self.vectorizer.fit_transform(self.study_texts)

    def merge_study_sections(self, documents: List[Document]) -> List[str]:
        """Fusionner les sections des études pour créer un texte unifié par étude."""
        study_texts = []

        # Dictionnaire pour regrouper les sections par study_id
        study_sections = {}

        # Regrouper le contenu des sections pour chaque étude
        for doc in documents:
            study_id = doc.metadata.get("study_id", "ID inconnu")
            section_content = doc.page_content

            if study_id not in study_sections:
                study_sections[study_id] = []

            study_sections[study_id].append(section_content)

        # Fusionner les sections pour chaque étude
        for study_id, sections in study_sections.items():
            full_text = " ".join(sections)  # Fusionner les sections par étude
            study_texts.append(full_text.strip())

        return study_texts

    def retrieve(self, query: str, k: int = 10) -> List[dict]:
        query_vec = self.vectorizer.transform([query])
        similarities = cosine_similarity(query_vec, self.tfidf_matrix).flatten()
        sorted_indices = np.argsort(similarities)[::-1]
        results = []
        for idx in sorted_indices[:k]:
            if similarities[idx] > 0:
                results.append({
                    "study_id": self.documents[idx].metadata["study_id"],
                    "score": similarities[idx],
                    "document": self.documents[idx]
                })
        return results

