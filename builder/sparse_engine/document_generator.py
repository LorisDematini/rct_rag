import json
import pickle
from config import ACRONYMS_FILE, SECTIONS_JSON_PATH, SPARSE_JSON_PATH, SPARSE_PCKL_PATH
from utils import preprocess
from langchain.schema import Document

def generator_save_documents(input_path: str = SECTIONS_JSON_PATH, acronyms_path: str = ACRONYMS_FILE, output_json: str = SPARSE_JSON_PATH, output_pkl: str = SPARSE_PCKL_PATH) -> None:
    """
    Processes section data from JSON, applies text preprocessing,
    and saves both the processed text (JSON) and LangChain Documents (Pickle).

    Args:
        input_path (str): Path to the raw section json.
        acronyms_path (str): Path to the final acronym file.
        output_json (str): Path where the processed section JSON will be saved.
    """

    # Load acronyms definitions
    with open(acronyms_path, 'r', encoding='utf-8') as file_acronym:
        acronyms_all = json.load(file_acronym)

    # Load raw section data
    with open(input_path, 'r', encoding='utf-8') as file_input:
        data_sections = json.load(file_input)

    processed_data = {}   # Contain the preprocessed text for each study
    documents = []        # Got the LangChain Document objects

    for study_id, sections in data_sections.items():
        if not isinstance(sections, dict):
            print(f"[WARN] Protocol {study_id} skipped (invalid sections format).")
            continue

        processed_sections = {}
        section_blocks = []

        for section_title, entries in sections.items():
            if not isinstance(entries, list):
                continue

            # Merge all text entries in the section
            section_texts = [entry for entry in entries if isinstance(entry, str)]
            merged_text = ' '.join(section_texts)

            # Apply preprocessing
            processed_text = preprocess(merged_text, study_id, acronyms_all)
            processed_sections[section_title] = processed_text

            # Store section text for document construction
            section_blocks.append(f"\n{processed_text}")

        processed_data[study_id] = processed_sections

        # Create a LangChain Document with all section texts
        full_text = '\n\n'.join(section_blocks)
        documents.append(Document(
            page_content=full_text,
            metadata={"study_id": study_id}
        ))

    # Save processed text as JSON
    with open(output_json, 'w', encoding='utf-8') as f_json:
        json.dump(processed_data, f_json, ensure_ascii=False, indent=2)

    # Save LangChain Documents as Pickle
    with open(output_pkl, 'wb') as f_pickle:
        pickle.dump(documents, f_pickle)

    print(f"Preprocessed text saved to: {output_json}")
    print(f"LangChain Documents saved to: {output_pkl}")
    
    return documents