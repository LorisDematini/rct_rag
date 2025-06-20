"""
data_loader.py

Ce module gère le chargement et la préparation des données utilisées par les moteurs de recherche
(sparse et dense). Il convertit les fichiers JSON en objets `Document` de LangChain, avec les
métadonnées nécessaires à la recherche et à l'affichage.

Fonctions :
- load_data_sparse() :
    Charge les documents prétraités pour le moteur sparse.
    Si le fichier n'existe pas, le génère à partir du RAW JSON.

- load_data_dense() :
    Charge les documents bruts sectionnés pour le moteur dense.
    Chaque section devient un objet `Document` avec un champ `field`.

- load_dense_sections(dense_json_path) :
    Charge les sections de texte issues du JSON dense prétraité,
    et les regroupe par `study_id` avec les champs associés.

"""


import os
from config.paths import SPARSE_JSON_PATH
from preprocess.processed_sparse  import process_and_merge_json

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
        