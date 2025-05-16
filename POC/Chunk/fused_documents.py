import json
import os

def fuse_json_documents(input_json):
    fused_docs = []
    for study_name, sections in input_json.items():
        content_lines = [f"{key}: {value}" for key, value in sections]
        full_text = "\n".join(content_lines)
        fused_docs.append({
            "page_content": full_text,
            "metadata": {"study": study_name}
        })
    return fused_docs

# Chemins
input_path = "/home/loris/Stage/STAGE/Test/db_sortie_block/DOC/POC/Clean/Search_engine/data/summary.json"
output_path = "/home/loris/Stage/STAGE/Test/db_sortie_block/DOC/Embedding/Chunk/fused_documents.json"

# Lecture
with open(input_path, "r", encoding="utf-8") as f:
    raw_json = json.load(f)

# Fusion
fused_documents = fuse_json_documents(raw_json)

# Sauvegarde
os.makedirs(os.path.dirname(output_path), exist_ok=True)
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(fused_documents, f, ensure_ascii=False, indent=2)

print(f"Fichier sauvegardé avec succès dans : {output_path}")
