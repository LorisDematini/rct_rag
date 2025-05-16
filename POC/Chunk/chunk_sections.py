import json
from transformers import AutoTokenizer

# Paramètres
MAX_TOKENS_PER_CHUNK = 384
MIN_TOKENS_PER_CHUNK = 100
MODEL_NAME = 'sentence-transformers/all-mpnet-base-v2'

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

def count_tokens(text):
    return len(tokenizer.encode(text, add_special_tokens=False))

def chunk_and_merge_sections(sections):
    """
    sections: list de dict {page_content, metadata: {study_id, field}}
    
    Retourne une liste de chunks, chaque chunk est dict:
    {
        "page_content": str,
        "metadata": {
            "study_id": str,
            "field": str (fusion des fields par concat si fusion)
        }
    }
    """

    chunks = []
    current_chunk_text = ""
    current_fields = []
    current_study_id = None

    def save_current_chunk():
        nonlocal current_chunk_text, current_fields, current_study_id
        if not current_chunk_text:
            return
        # fusionne les fields distincts en une string séparée par " | "
        merged_field = " | ".join(dict.fromkeys(current_fields))
        chunks.append({
            "page_content": current_chunk_text.strip(),
            "metadata": {
                "study_id": current_study_id,
                "field": merged_field
            }
        })
        current_chunk_text = ""
        current_fields = []

    for section in sections:
        text = section["page_content"].strip()
        study_id = section["metadata"]["study_id"]
        field = section["metadata"]["field"]

        # Initialisation de study_id si premier chunk
        if current_study_id is None:
            current_study_id = study_id

        # Compter tokens si on ajoute cette section au chunk courant
        new_text = (current_chunk_text + " " + text).strip() if current_chunk_text else text
        new_tokens = count_tokens(new_text)

        if new_tokens <= MAX_TOKENS_PER_CHUNK:
            # On peut ajouter cette section au chunk courant
            current_chunk_text = new_text
            current_fields.append(field)
        else:
            # Sinon on sauvegarde le chunk courant et on démarre un nouveau
            save_current_chunk()
            # On met cette section dans un nouveau chunk (même study_id)
            current_chunk_text = text
            current_fields = [field]

    # Sauvegarde dernier chunk restant
    save_current_chunk()

    # Fusion des chunks trop petits avec leurs voisins (uniquement avec le précédent)
    merged_chunks = []
    for chunk in chunks:
        chunk_tokens = count_tokens(chunk["page_content"])
        if chunk_tokens < MIN_TOKENS_PER_CHUNK and merged_chunks:
            # Fusionne avec chunk précédent
            prev = merged_chunks[-1]
            combined_text = prev["page_content"] + " " + chunk["page_content"]
            combined_fields = prev["metadata"]["field"] + " | " + chunk["metadata"]["field"]
            combined_study_id = prev["metadata"]["study_id"]  # suppose identique

            merged_chunks[-1] = {
                "page_content": combined_text.strip(),
                "metadata": {
                    "study_id": combined_study_id,
                    "field": " | ".join(dict.fromkeys(combined_fields.split(" | ")))  # unique fields
                }
            }
        else:
            merged_chunks.append(chunk)

    return merged_chunks


# Exemple d'utilisation
if __name__ == "__main__":
    # Ici tu charges tes sections depuis un JSON ou autre
    input_path = "/home/loris/Stage/STAGE/Test/db_sortie_block/DOC/Chunk/summaryDense_pre.json"
    output_path = "/home/loris/Stage/STAGE/Test/db_sortie_block/DOC/Chunk/chunked_sections.json"

    with open(input_path, "r", encoding="utf-8") as f:
        sections = json.load(f)

    chunked_sections = chunk_and_merge_sections(sections)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(chunked_sections, f, ensure_ascii=False, indent=2)

    print(f"{len(chunked_sections)} chunks sauvegardés dans {output_path}")
