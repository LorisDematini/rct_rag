# /core/data_loader.py

import os
import json
from langchain.schema import Document
from config.paths import TFIDF_JSON_PATH, RAW_JSON_PATH
from preprocess.processed_tfidf  import process_and_merge_json

def ensure_tfidf_preprocessed_json():
    if not os.path.exists(TFIDF_JSON_PATH):
        print(f"[INFO] Le fichier TF-IDF prétraité est introuvable. Génération en cours...")

        with open(RAW_JSON_PATH, 'r', encoding='utf-8') as f:
            raw_data = json.load(f)

        merged = process_and_merge_json(raw_data)

        with open(TFIDF_JSON_PATH, 'w', encoding='utf-8') as f:
            json.dump(merged, f, ensure_ascii=False, indent=2)

    else:
        print(f"[INFO] Fichier TF-IDF déjà existant : {TFIDF_JSON_PATH}")


def load_data_tfidf():
    ensure_tfidf_preprocessed_json()

    with open(TFIDF_JSON_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    documents = []
    for study_id, sections in data.items():
        if isinstance(sections, dict):  # les sections ont déjà été prétraitées
            merged_text = " ".join(sections.values())
            documents.append(
                Document(
                    page_content=merged_text,
                    metadata={"study_id": study_id}
                )
            )
    print(f"[INFO] Études chargées : {len(documents)}")
    return documents

def load_data_embeddings():
    with open(RAW_JSON_PATH, "r", encoding="utf-8") as f:
        raw_data = json.load(f)

    documents = []

    # Si c'est un dictionnaire (structure attendue dans ce cas)
    if isinstance(raw_data, dict):
        for study_id, texts in raw_data.items():
            # On parcourt chaque élément de la liste pour en extraire le contenu
            for pair in texts:
                if len(pair) == 2 and isinstance(pair[1], str):  # Assurer que la valeur est du texte
                    documents.append(Document(
                        page_content=pair[1],  # Texte dans la seconde position
                        metadata={"study_id": study_id, "field": pair[0]}  # Enregistrer l'identifiant et le champ
                    ))
        print(f"[INFO] Documents convertis à partir du dict : {len(documents)}")
        return documents

    # Si c'est une liste (structure déjà en format acceptable)
    elif isinstance(raw_data, list):
        for entry in raw_data:
            if isinstance(entry, dict) and "page_content" in entry:
                documents.append(Document(
                    page_content=entry["page_content"],
                    metadata=entry.get("metadata", {})
                ))
        print(f"[INFO] Documents chargés à partir de la liste : {len(documents)}")
        return documents

    raise ValueError("[ERREUR] Le fichier JSON doit contenir une liste ou un dictionnaire.")

