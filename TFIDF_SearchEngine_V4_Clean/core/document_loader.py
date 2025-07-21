import json
from config.paths import ACRONYMS_FILE, SECTIONS_FULL_JSON_PATH, EXACT_JSON_PATH, SECTIONS_JSON_PATH, SPARSE_JSON_PATH
from preprocess.processed_exact import preprocess_ex
from preprocess.processed_sparse import preprocess
from langchain.schema import Document


def creation_apply_exact(input_path=SECTIONS_FULL_JSON_PATH, output_path=EXACT_JSON_PATH ):
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
                    section_texts.append(entry)

            merged_text = ' '.join(section_texts)
            processed_text = preprocess_ex(merged_text)
            processed_sections[section_title] = processed_text

        processed_data[study_id] = processed_sections

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(processed_data, f, ensure_ascii=False, indent=2)

    return processed_data


def creation_apply_sparse(input_path=SECTIONS_JSON_PATH, acronyms_path=ACRONYMS_FILE, output_path=SPARSE_JSON_PATH ):
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


def document_exact(existing=False):
    if not(existing):
        data = creation_apply_exact()

    else :
        with open(EXACT_JSON_PATH, 'r', encoding='utf-8') as f:
            data = json.load(f)
    
    documents = []

    for study_id, sections in data.items():
        if not isinstance(sections, dict):
            print(f"[WARN] protocole {study_id} ignoré (sections non valides).")
            continue

        for section_name, content in sections.items():
            if not isinstance(content, str):
                continue

            doc = Document(
                page_content=content,
                metadata={
                    "study_id": study_id,
                    "section_name": section_name
                }
            )
            documents.append(doc)

    print(f"[INFO] Documents générés (par section) : {len(documents)}")
    return documents


def document_sparse(existing=False):
    if not(existing):
        data = creation_apply_sparse()

    else :
        with open(SPARSE_JSON_PATH, 'r', encoding='utf-8') as f:
            data = json.load(f)
    
    documents = []

    for study_id, sections in data.items():
        if not isinstance(sections, dict):
            print(f"[WARN] protocole {study_id} ignoré (sections non valides).")
            continue

        # On garde les noms de sections
        section_blocks = []
        for section_name, content in sections.items():
            section_blocks.append(f"[{section_name}]\n{content}")

        full_text = '\n\n'.join(section_blocks)

        documents.append(Document(
            page_content=full_text,
            metadata={"study_id": study_id}
        ))

    print(f"Documents générés : {len(documents)}")
    return documents