import os

# Racine du projet
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Dossier des données JSON (textes à indexer)
DATA_DIR = os.path.join(BASE_DIR, "data")
RAW_JSON_PATH = os.path.join(DATA_DIR, "summary.json")  # Nom du fichier JSON contenant les documents RAW
ACRONYMS_FILE = os.path.join(DATA_DIR, "final_acronyms.json")  # Fichier contenant les acronymes et leurs définitions

# Fichier de sortie prétraité spécifique au moteur TF-IDF
TFIDF_JSON_PATH = os.path.join(DATA_DIR, "summaryTF_pre.json")

DOC_DUMP_PATH = os.path.join(DATA_DIR, "documents_used_for_index.json")

# Fichier de sortie prétraité spécifique au moteur Embedding
EMB_JSON_PATH = os.path.join(DATA_DIR, "summaryEMB_pre.json")

# Fichier de sortie prétraité spécifique au moteur FAISS
FAISS_JSON_PATH = os.path.join(DATA_DIR, "summaryFA_pre.json")

FAISS_INDEX_PATH = os.path.join(DATA_DIR, "faiss_index")  # Répertoire pour l'index FAISS
