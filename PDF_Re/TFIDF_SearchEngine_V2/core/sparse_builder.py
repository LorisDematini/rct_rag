"""
sparse_index_builder.py

Ce module construit un index TF-IDF à partir d'une liste de documents LangChain.
Il regroupe soit :
- les sections d'une même étude (ancienne version, voir code commenté),
- soit toutes les sections d’un même type (nouvelle version, par section globale),
et génère une matrice sparse utilisable pour la recherche textuelle.
"""

from typing import List
from langchain.schema import Document
from sklearn.feature_extraction.text import TfidfVectorizer


#TF-IDF par étude ===
class SparseBuilder:
    def __init__(self, documents: List[Document]):
        self.documents = documents
        self.study_ids = []
        self.study_texts = self.merge_study_sections(documents)
        self.vectorizer = TfidfVectorizer(max_df=0.95)
        self.sparse_matrix = self.vectorizer.fit_transform(self.study_texts)

    def merge_study_sections(self, documents: List[Document]) -> List[str]:
        study_texts = []
        study_sections = {}

        for doc in documents:
            study_id = doc.metadata.get("study_id", "ID inconnu")
            section_content = doc.page_content

            if study_id not in study_sections:
                study_sections[study_id] = []

            study_sections[study_id].append(section_content)

        for study_id, sections in study_sections.items():
            full_text = " ".join(sections)
            study_texts.append(full_text.strip())
            self.study_ids.append(study_id)

        return study_texts


# TF-IDF par section 
# class SparseBuilder:
#     """
#     Construit un index TF-IDF en regroupant tous les contenus d'une même section 
#     (ex: tous les TITLES, tous les OBJECTIVES...) sur l'ensemble des études.
#     """
#     def __init__(self, documents: List[Document]):
#         self.documents = documents

#         # Noms des sections globales : TITLE, JUSTIFICATION, etc.
#         self.section_names = []

#         # Liste des textes fusionnés par section
#         self.section_texts = self.merge_by_section(documents)

#         # TF-IDF vectorizer
#         self.vectorizer = TfidfVectorizer(max_df=0.95)
#         self.sparse_matrix = self.vectorizer.fit_transform(self.section_texts)

#     def merge_by_section(self, documents: List[Document]) -> List[str]:
#         section_groups: Dict[str, List[str]] = {}

#         for doc in documents:
#             section = doc.metadata.get("section", "UNKNOWN")
#             content = doc.page_content

#             if section not in section_groups:
#                 section_groups[section] = []

#             section_groups[section].append(content)

#         # On garde la trace de l’ordre des sections
#         self.section_names = list(section_groups.keys())

#         return [" ".join(texts).strip() for texts in section_groups.values()]