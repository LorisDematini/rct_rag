import os

# Project root
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "Data")

# Folder containing the original PDF files
PDF_FOLDER = os.path.join(DATA_DIR, "pdf")

# JSON file containing raw extracted text from PDFs
SUMMARY_JSON_PATH = os.path.join(DATA_DIR, "summary.json")

# Acronym-related JSON files
ACRONYMS_EXTRACT_PATH = os.path.join(DATA_DIR, "acronym_extracted_pdf.json")
ACRONYMS_STUDY_PATH = os.path.join(DATA_DIR, "acronyms_etude.json")
ACRONYMS_FILE = os.path.join(DATA_DIR, "extracted_acronym_final.json")
ACRONYMS_FILE_UNIQUE = os.path.join(DATA_DIR, "unique_acronym.json")

# Section-related JSON files
SECTIONS_JSON_PATH = os.path.join(DATA_DIR, "sections_sorted.json")
SECTIONS_FULL_JSON_PATH = os.path.join(DATA_DIR, "sections_sorted_full.json")

# Processed and complete TFIDF files 
SPARSE_JSON_PATH = os.path.join(DATA_DIR, "summarySparse_pre.json")
SPARSE_PCKL_PATH = os.path.join(DATA_DIR, "document_sparse.pkl")

# Processed and complete Exact/Key-Words files 
EXACT_JSON_PATH = os.path.join(DATA_DIR, "summaryExact_pre.json")
EXACT_PCKL_PATH = os.path.join(DATA_DIR, "document_exact.pkl")

#Available Sections 
AVAILABLE_SECTIONS_JSON_PATH = os.path.join(DATA_DIR, "list_sections.json")

#top terms
TOP_TERMS_PATH = os.path.join(DATA_DIR, "TopTermsByStudy.json")

#Vectorizer
VECTOR_PATH = os.path.join(DATA_DIR, "vectorizer.pkl")
MATRIX_PATH = os.path.join(DATA_DIR, "sparse_matrix.npz")
STUDY_IDS_PATH = os.path.join(DATA_DIR, "study_ids.npy")