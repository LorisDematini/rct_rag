from langchain.schema import Document
import json
from config.paths import  ACRONYMS_FILE, SPARSE_JSON_PATH, SECTIONS_JSON_PATH
from preprocess.processed_sparse import preprocess


def process_and_merge_sections(input_path=SECTIONS_JSON_PATH, acronyms_path=ACRONYMS_FILE, output_path=SPARSE_JSON_PATH ):
    with open(acronyms_path, 'r', encoding='utf-8') as f:
        acronyms_all = json.load(f)

    with open(input_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    processed_data = {}

    for study_id, sections in data.items():
        if not isinstance(sections, dict):
            print(f"[WARN] protocole {study_id} ignoré (sections non valides).")
            continue

        processed_sections = {}

        for section_title, entries in sections.items():
            if not isinstance(entries, list):
                continue

            # Fusionne les entrées de la section
            section_texts = []
            for entry in entries:
                if isinstance(entry, str):
                    #Retirer les titres si besoin 
                    # if ':' in entry:
                    #     entry = entry.split(':', 1)[1].strip()
                    section_texts.append(entry)

            merged_text = ' '.join(section_texts)
            processed_text = preprocess(merged_text, study_id, acronyms_all)
            processed_sections[section_title] = processed_text

        processed_data[study_id] = processed_sections

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(processed_data, f, ensure_ascii=False, indent=2)

    return processed_data

def process_and_merge_json(existing=False):
    if not existing:
        data = process_and_merge_sections()
    else:
        with open(SPARSE_JSON_PATH, 'r', encoding='utf-8') as f:
            data = json.load(f)

    documents = []

    for study_id, sections in data.items():
        if not isinstance(sections, dict):
            continue

        for section_name, content in sections.items():
            if isinstance(content, str) and content.strip():
                documents.append(Document(
                    page_content=content.strip(),
                    metadata={
                        "study_id": study_id,
                        "section_name": section_name
                    }
                ))

    return documents