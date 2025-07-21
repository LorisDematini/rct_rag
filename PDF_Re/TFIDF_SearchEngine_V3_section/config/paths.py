import os

# Racine du projet
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")

#Dossier contenant les fichiers d'origine docx
PDF_FOLDER = os.path.join(DATA_DIR, "pdf")

#Fichiers d'entrées contenant les données du texte
SECTIONS_JSON_PATH = os.path.join(DATA_DIR, "sections_sorted.json")
SECTIONS_FULL_JSON_PATH = os.path.join(DATA_DIR, "sections_sorted_full.json")
SUMMARY_JSON_PATH = os.path.join(DATA_DIR, "summary.json")

#Fichiers contenant les acronymes du texte
ACRONYMS_FILE = os.path.join(DATA_DIR, "extracted_acronym_final.json")
ACRONYMS_FILE_UNIQUE = os.path.join(DATA_DIR, "unique_acronym.json")

# Fichier de sortie prétraité spécifique aux moteurs
SPARSE_JSON_PATH = os.path.join(DATA_DIR, "summarySparse_pre.json")
EXACT_JSON_PATH = os.path.join(DATA_DIR, "summaryExact_pre.json")

#OLD RAW
# RAW_JSON_PATH = os.path.join(DATA_DIR, "summary.json")  # Nom du fichier JSON contenant les documents RAW