import json
import pickle
from langchain.schema import Document
from utils import preprocess_ex

def generate_save_exact_documents(input_path, output_json, output_pkl):
    """
    Loads raw study sections from a JSON file, applies text preprocessing
    section by section, saves the cleaned text into a JSON file,
    and serializes LangChain Document objects into a Pickle file.

    Args:
        input_path (str): Path to the raw JSON input containing study sections.
        output_json (str): Path to save the preprocessed section texts in JSON format.
        output_pkl (str): Path to save the LangChain Document list in Pickle format.

    Returns:
        list: A list of LangChain Document objects (one per section).
    """

    # Load raw section data
    with open(input_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    processed_data = {}  # Dictionary to store the preprocessed text per study
    documents = []       # List to store LangChain Document objects

    for study_id, sections in data.items():
        if not isinstance(sections, dict):
            print(f"[WARN] Study {study_id} skipped (invalid section format).")
            continue

        processed_sections = {}

        for section_title, entries in sections.items():
            if not isinstance(entries, list):
                continue

            # Merge all string entries in the section
            section_texts = [entry for entry in entries if isinstance(entry, str)]
            merged_text = ' '.join(section_texts)

            # Apply custom preprocessing
            processed_text = preprocess_ex(merged_text)
            processed_sections[section_title] = processed_text

            # Create a LangChain Document for this section
            doc = Document(
                page_content=processed_text,
                metadata={
                    "study_id": study_id,
                    "section_name": section_title
                }
            )
            documents.append(doc)

        # Store all preprocessed sections for this study
        processed_data[study_id] = processed_sections

    # Save preprocessed text to JSON
    with open(output_json, 'w', encoding='utf-8') as f_json:
        json.dump(processed_data, f_json, ensure_ascii=False, indent=2)

    # Save Document objects to Pickle
    with open(output_pkl, 'wb') as f_pickle:
        pickle.dump(documents, f_pickle)

    # Logs
    print(f"[INFO] Preprocessed text saved to: {output_json}")
    print(f"[INFO] LangChain Documents saved to: {output_pkl}")
    print(f"[INFO] Total documents created: {len(documents)}")

    return documents
