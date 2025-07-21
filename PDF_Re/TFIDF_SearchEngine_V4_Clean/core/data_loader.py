import os
from config.paths import EXACT_JSON_PATH, SPARSE_JSON_PATH
from core.document_loader import document_exact, document_sparse


def load_data_sparse():
    if not os.path.exists(SPARSE_JSON_PATH):
        print(f"[INFO] Le fichier SPARSE_JSON est introuvable. Génération en cours...")

        # Génère les documents et sauvegarde aussi un JSON
        documents = document_sparse()
        return documents

    else:
        print(f"[INFO] Fichier SPARSE déjà existant : {SPARSE_JSON_PATH}")
        documents = document_sparse(existing=True)
        return documents
        
def load_data_exact():
    if not os.path.exists(EXACT_JSON_PATH):
        print(f"[INFO] Le fichier EXACT_JSON est introuvable. Génération en cours...")

        # Génère les documents
        documents = document_exact()
        return documents

    else:
        print(f"[INFO] Fichier JSON déjà existant : {EXACT_JSON_PATH}")
        documents = document_exact(existing=True)
        return documents