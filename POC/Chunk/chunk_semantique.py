import os
import re
import json
import nltk
from scipy.spatial.distance import cosine
from sentence_transformers import SentenceTransformer
from transformers import AutoTokenizer

# Téléchargement NLTK pour la tokenisation
nltk.download('punkt')

# === Paramètres ===
SEMANTIC_THRESHOLD = 0.3
MAX_TOKENS_PER_CHUNK = 384
MIN_TOKENS_PER_CHUNK = 100
MODEL_NAME = 'sentence-transformers/all-mpnet-base-v2'

# Chargement du modèle et du tokenizer
model = SentenceTransformer(MODEL_NAME)
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

# === Chemins ===
input_path = "/home/loris/Stage/STAGE/Test/db_sortie_block/DOC/Chunk/fused_documents_pre.json"
output_path = "/home/loris/Stage/STAGE/Test/db_sortie_block/DOC/Chunk/semantic_chunks.json"

# === Fonction pour obtenir les embeddings ===
def get_embeddings(sentences):
    return model.encode(
        sentences,
        convert_to_numpy=True,
        show_progress_bar=False,
        batch_size=32,
        normalize_embeddings=False
    )

# === Fonction de découpe par tokens si chunk trop long ===
def split_large_chunk_by_tokens(chunk, max_tokens):
    sentences = re.split(r'(?<=[.!?]) +|\n+|; +', chunk)
    sentences = [s.strip() for s in sentences if s.strip()]
    chunks = []
    current = []
    current_token_count = 0

    for sent in sentences:
        sent_tokens = tokenizer.encode(sent, add_special_tokens=False)
        if current_token_count + len(sent_tokens) > max_tokens:
            if current:
                chunk_text = " ".join(current).strip()
                if chunk_text:
                    chunks.append(chunk_text)
            current = []
            current_token_count = 0
        current.append(sent)
        current_token_count += len(sent_tokens)

    if current:
        chunk_text = " ".join(current).strip()
        if chunk_text:
            chunks.append(chunk_text)

    return chunks

# === Fusion des petits chunks avec leurs voisins ===
def merge_small_chunks(chunks, min_tokens, max_tokens):
    merged = []
    i = 0
    while i < len(chunks):
        current = chunks[i]
        current_tokens = tokenizer.encode(current, add_special_tokens=False)

        if len(current_tokens) < min_tokens:
            # Tenter de fusionner avec le chunk précédent
            if merged:
                prev = merged[-1]
                prev_tokens = tokenizer.encode(prev, add_special_tokens=False)
                if len(prev_tokens) + len(current_tokens) <= max_tokens:
                    merged[-1] = prev + " " + current
                    i += 1
                    continue
            # Sinon, tenter de fusionner avec le chunk suivant
            elif i + 1 < len(chunks):
                next_chunk = chunks[i + 1]
                next_tokens = tokenizer.encode(next_chunk, add_special_tokens=False)
                if len(current_tokens) + len(next_tokens) <= max_tokens:
                    chunks[i + 1] = current + " " + next_chunk
                    i += 1
                    continue

        merged.append(current)
        i += 1

    return merged

# === Fonction principale de chunking sémantique ===
def semantic_chunk_document(text, metadata):
    text = text.replace('\n', ' ').replace('  ', ' ').strip()
    if not text:
        return []

    sentences = re.split(r'(?<=[.!?]) +|\n+|; +', text)
    sentences = [s.strip() for s in sentences if s.strip()]
    if not sentences:
        return []

    # Troncature des phrases trop longues (512 tokens max pour mpnet)
    filtered_sentences = []
    for sent in sentences:
        tokens = tokenizer.encode(sent, add_special_tokens=False)
        if len(tokens) <= 512:
            filtered_sentences.append(sent)
        else:
            truncated = tokenizer.decode(tokens[:512], skip_special_tokens=True, clean_up_tokenization_spaces=True)
            filtered_sentences.append(truncated)

    embeddings = get_embeddings(filtered_sentences)

    # Regroupement sémantique
    chunks = []
    current_chunk = [filtered_sentences[0]]

    for i in range(1, len(filtered_sentences)):
        sim = 1 - cosine(embeddings[i], embeddings[i - 1])
        if sim < (1 - SEMANTIC_THRESHOLD):
            chunk_text = " ".join(current_chunk).strip()
            if chunk_text:
                chunks.append(chunk_text)
            current_chunk = [filtered_sentences[i]]
        else:
            current_chunk.append(filtered_sentences[i])

    if current_chunk:
        chunk_text = " ".join(current_chunk).strip()
        if chunk_text:
            chunks.append(chunk_text)

    # Rechunk si chunk > max_tokens
    final_chunks = []
    for chunk in chunks:
        chunk_tokens = tokenizer.encode(chunk, add_special_tokens=False)
        if len(chunk_tokens) > MAX_TOKENS_PER_CHUNK:
            final_chunks.extend(split_large_chunk_by_tokens(chunk, MAX_TOKENS_PER_CHUNK))
        else:
            chunk_text = chunk.strip()
            if chunk_text:
                final_chunks.append(chunk_text)

    # Fusion des petits chunks avec leurs voisins
    merged_chunks = merge_small_chunks(final_chunks, MIN_TOKENS_PER_CHUNK, MAX_TOKENS_PER_CHUNK)

    # Suppression doublons et vides
    seen = set()
    unique_chunks = []
    for chunk in merged_chunks:
        if chunk and chunk not in seen:
            unique_chunks.append(chunk)
            seen.add(chunk)

    return [
        {
            "page_content": chunk,
            "metadata": {
                "study": metadata["study"],
                "chunk_id": i
            }
        }
        for i, chunk in enumerate(unique_chunks)
    ]

# === Traitement global ===
with open(input_path, "r", encoding="utf-8") as f:
    fused_documents = json.load(f)

semantic_chunks = []
for doc in fused_documents:
    chunks = semantic_chunk_document(doc["page_content"], doc["metadata"])
    semantic_chunks.extend(chunks)

# === Sauvegarde JSON ===
os.makedirs(os.path.dirname(output_path), exist_ok=True)
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(semantic_chunks, f, ensure_ascii=False, indent=2)

print(f"{len(semantic_chunks)} semantic chunks sauvegardés dans : {output_path}")