import pickle
import numpy as np
from scipy import sparse
from sklearn.feature_extraction.text import TfidfVectorizer
from Config import VECTOR_PATH, MATRIX_PATH, STUDY_IDS_PATH

def build_save_sparse_index(documents):
    """
    Builds and saves a sparse TF-IDF index from a list of LangChain Document objects.

    Args:
        documents (List[Document]): A list of LangChain Document objects. Each document must have:
            - .page_content: The textual content of the section.
            - .metadata["study_id"]: The identifier for the corresponding study.

    Returns:
        tuple: (vectorizer, sparse_matrix, study_ids)
            - vectorizer: The fitted TfidfVectorizer object.
            - sparse_matrix: The TF-IDF sparse matrix (scipy.sparse.csr_matrix).
            - study_ids: List of study IDs (in the same order as in the matrix).
    """

    study_ids = []          # Will store the final list of study IDs
    study_sections = {}     # Dictionary to group sections by study ID
    study_texts = []        # Final list of full texts (one per study)

    # Group sections by their corresponding study_id
    for doc in documents:
        study_id = doc.metadata.get("study_id", "ID inconnu")  # Default if study_id missing
        section_content = doc.page_content
        if study_id not in study_sections:
            study_sections[study_id] = []
        study_sections[study_id].append(section_content)

    # Concatenate all sections for each study into a single text
    for study_id, sections in study_sections.items():
        full_text = " ".join(sections)
        study_texts.append(full_text.strip())
        study_ids.append(study_id)

    # Build the TF-IDF sparse matrix
    vectorizer = TfidfVectorizer(max_df=0.95)
    sparse_matrix = vectorizer.fit_transform(study_texts)

    # Save the vectorizer
    with open(VECTOR_PATH, "wb") as f:
        pickle.dump(vectorizer, f)

    # Save the sparse TF-IDF matrix
    sparse.save_npz(MATRIX_PATH, sparse_matrix)

    # Save the list of study IDs
    np.save(STUDY_IDS_PATH, np.array(study_ids))

    # Log confirmation
    print(f"Vectorizer saved to: {VECTOR_PATH}")
    print(f"Matrix sparse saved to: {MATRIX_PATH}")
    print(f"List of Study_ids: {STUDY_IDS_PATH}")

    return vectorizer, sparse_matrix, study_ids
