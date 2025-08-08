"""
paths.py

This python file defines paths to all files and directories used in the project.

Path organization:
- Root: `BASE_DIR`, `PARENT OF BASE`, `BUILDER` and `DATA_DIR` define the base structure of the project.
- PDF files: folder containing the source pdf documents (`PDF_FOLDER`).
- JSON files:
    - `SECTIONS_JSON_PATH`, `SUMMARY_JSON_PATH`: contain processed and summarized document content.
    - `ACRONYMS_FILE`, `ACRONYMS_FILE_UNIQUE`: store extracted acronyms and their deduplicated version.
    - `TOP_TERMS_PATH`: top TF-IDF terms per document.
- Sparse search engine files:
    - `VECTOR_PATH`, `MATRIX_PATH`, `STUDY_IDS_PATH`: store the TF-IDF vectorizer, the sparse matrix, and the study identifiers.
    - `SPARSE_PCKL_PATH`: LangChain documents used in sparse retrieval (pickled format).
"""

import os

# Project root directories
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PARENT_OF_BASE = os.path.dirname(BASE_DIR)
BUILDER = os.path.join(PARENT_OF_BASE, "Builder")
DATA_DIR = os.path.join(BUILDER, "Data")

# Folder containing the original source files (PDF or DOCX)
PDF_FOLDER = os.path.join(DATA_DIR, "pdf")

# JSON file containing raw summaries for each study
SUMMARY_JSON_PATH = os.path.join(DATA_DIR, "summary.json")

# JSON files containing acronym definitions
ACRONYMS_FILE = os.path.join(DATA_DIR, "extracted_acronym_final.json")
ACRONYMS_FILE_UNIQUE = os.path.join(DATA_DIR, "unique_acronym.json")

# JSON file with cleaned and sorted section content
SECTIONS_JSON_PATH = os.path.join(DATA_DIR, "sections_sorted.json")
SECTIONS_FULL_JSON_PATH = os.path.join(DATA_DIR, "sections_sorted_full.json")

# Pickled list of LangChain Documents for sparse retrieval
SPARSE_PCKL_PATH = os.path.join(DATA_DIR, "document_sparse.pkl")

# Pickled list of LangChain Documents for exact retrieval
EXACT_PCKL_PATH = os.path.join(DATA_DIR, "document_exact.pkl")

#Available sections
AVAILABLE_SECTIONS_JSON_PATH = os.path.join(DATA_DIR, "list_sections.json")

# TF-IDF components
VECTOR_PATH = os.path.join(DATA_DIR, "vectorizer.pkl")
MATRIX_PATH = os.path.join(DATA_DIR, "sparse_matrix.npz")
STUDY_IDS_PATH = os.path.join(DATA_DIR, "study_ids.npy")

# JSON file listing top TF-IDF terms for each study
TOP_TERMS_PATH = os.path.join(DATA_DIR, "TopTermsByStudy.json")
