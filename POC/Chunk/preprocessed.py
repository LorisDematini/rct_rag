import json
import sys

# --- Ajout du chemin vers le dossier contenant processed_dense.py ---
preprocess_path = "/home/loris/Stage/STAGE/Test/db_sortie_block/DOC/POC/Clean/Search_engine/preprocess"
if preprocess_path not in sys.path:
    sys.path.append(preprocess_path)

from processed_dense import TextPreprocessor

def preprocess_sections(input_json_path, output_json_path):
    # Charger le JSON
    with open(input_json_path, "r", encoding="utf-8") as f:
        sections = json.load(f)

    preprocessor = TextPreprocessor()

    # Traiter chaque section
    for section in sections:
        original_text = section.get("page_content", "")
        processed_text = preprocessor.preprocess(original_text)
        section["page_content"] = processed_text

    # Sauvegarder le résultat
    with open(output_json_path, "w", encoding="utf-8") as f:
        json.dump(sections, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    input_path = "/home/loris/Stage/STAGE/Test/db_sortie_block/DOC/Chunk/fused_documents.json"
    output_path = "/home/loris/Stage/STAGE/Test/db_sortie_block/DOC/Chunk/fused_documents_pre.json"
    preprocess_sections(input_path, output_path)
    print(f"Prétraitement terminé. Résultats sauvegardés dans {output_path}")
