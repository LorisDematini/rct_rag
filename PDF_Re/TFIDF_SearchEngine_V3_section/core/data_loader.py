import os
from config.paths import EXACT_JSON_PATH, SPARSE_JSON_PATH
from preprocess.processed_exact import process_and_keep_json
from core.document_loader_sparse  import process_and_merge_json

def load_data_sparse():
    if not os.path.exists(SPARSE_JSON_PATH):
        print(f"[INFO] Le fichier SPARSE_JSON est introuvable. Génération en cours...")

        # Génère les documents et sauvegarde aussi un JSON
        documents = process_and_merge_json()
        return documents

    else:
        print(f"[INFO] Fichier SPARSE déjà existant : {SPARSE_JSON_PATH}")
        documents = process_and_merge_json(existing=True)
        return documents
        
def load_data_exact():
    if not os.path.exists(EXACT_JSON_PATH):
        print(f"[INFO] Le fichier EXACT_JSON est introuvable. Génération en cours...")

        # Génère les documents
        documents = process_and_keep_json()
        return documents

    else:
        print(f"[INFO] Fichier JSON déjà existant : {EXACT_JSON_PATH}")
        documents = process_and_keep_json(existing=True)
        return documents