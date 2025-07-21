import re
import json
from nltk.corpus import stopwords
from langchain.schema import Document
from config.paths import EXACT_JSON_PATH, SECTIONS_FULL_JSON_PATH

# nltk.download('punkt')
# nltk.download('averaged_perceptron_tagger')
# nltk.download('wordnet')
# nltk.download('stopwords')

def preprocess_ex(text):
    #minuscules
    text = text.lower()
    #ponctuation
    text = re.sub(r'[^\w\s*-]|_', ' ', text)
    text = text.replace("-", "")
    print(text)

    return text

def preprocess_query(query):
    query_cleaned = preprocess_ex(query)
    return query_cleaned


def process_and_keep_sections(input_path=SECTIONS_FULL_JSON_PATH, output_path=EXACT_JSON_PATH ):

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


def process_and_keep_json(existing=False):

    if not(existing):
        data = process_and_keep_sections()

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