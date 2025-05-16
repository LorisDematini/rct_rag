import os
import json
from transformers import AutoTokenizer
from sentence_transformers import SentenceTransformer

# === Paramètres ===
MAX_TOKENS_PER_CHUNK = 384
model_name = 'sentence-transformers/all-mpnet-base-v2'
model = SentenceTransformer(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)

# === Chemins ===
input_path = "/home/loris/Stage/STAGE/Test/db_sortie_block/DOC/Chunk/fused_documents_pre.json"
output_path = "/home/loris/Stage/STAGE/Test/db_sortie_block/DOC/Chunk/chunked_documents.json"

# === Chargement JSON ===
with open(input_path, "r", encoding="utf-8") as f:
    fused_documents = json.load(f)

def chunk_by_token_limit(text, metadata, max_tokens=MAX_TOKENS_PER_CHUNK):
    tokens = tokenizer.encode(text, add_special_tokens=False)
    chunks = []
    i = 0
    while i < len(tokens):
        chunk_tokens = tokens[i:i + max_tokens]
        chunk_text = tokenizer.decode(chunk_tokens, skip_special_tokens=True, clean_up_tokenization_spaces=True)
        chunks.append({
            "page_content": chunk_text,
            "metadata": {
                "study": metadata["study"],
                "chunk_id": len(chunks)
            }
        })
        i += max_tokens
    return chunks

# === Traitement global ===
token_chunks = []
for doc in fused_documents:
    token_chunks.extend(chunk_by_token_limit(doc["page_content"], doc["metadata"]))

# === Sauvegarde ===
os.makedirs(os.path.dirname(output_path), exist_ok=True)
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(token_chunks, f, ensure_ascii=False, indent=2)

print(f"{len(token_chunks)} token chunks sauvegardés dans : {output_path}")
