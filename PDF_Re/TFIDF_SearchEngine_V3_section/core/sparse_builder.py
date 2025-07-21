from sklearn.feature_extraction.text import TfidfVectorizer
from collections import defaultdict


def merge_study_sections(documents):
    study_texts = []
    study_ids = []
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
        study_ids.append(study_id)

    return study_texts, study_ids

def build_sparse_index(documents):
    section_texts = defaultdict(list)
    section_metadata = defaultdict(list)

    for doc in documents:
        section = doc.metadata.get("section_name", "Unknown")
        section_texts[section].append(doc.page_content)
        section_metadata[section].append(doc.metadata)

    vectorizers = {}
    sparse_matrices = {}

    for section_name, texts in section_texts.items():
        vectorizer = TfidfVectorizer()
        matrix = vectorizer.fit_transform(texts)
        vectorizers[section_name] = vectorizer
        sparse_matrices[section_name] = matrix

    return vectorizers, sparse_matrices, section_metadata

