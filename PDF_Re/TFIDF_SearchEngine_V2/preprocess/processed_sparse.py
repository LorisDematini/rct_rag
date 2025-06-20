"""
sparse_preprocessing.py

Ce module fournit une classe `TextPreprocessor` et des fonctions utilitaires pour nettoyer,
normaliser et fusionner les textes des études en vue de la vectorisation TF-IDF.

Fonctionnalités principales :
- Nettoyage des caractères spéciaux, normalisation Unicode et mise en minuscules.
- Lemmatisation et suppression des stop words standards et médicaux.
- Remplacement des acronymes selon un dictionnaire JSON.
- Standardisation de termes temporels (ex. "d10" → "day 10").
- Fusion des sections par étude en un seul document.
- Filtrage des termes trop fréquents selon un seuil `max_df` (comme en TF-IDF).
- Génération d’un fichier JSON contenant les textes fusionnés et filtrés.

Classes :
- TextPreprocessor :
    - normalize_text(text) : nettoie et lemmatise un texte brut.
    - replace_acronyms(text) : remplace les acronymes selon le dictionnaire.
    - replace_special_terms(text) : harmonise les notations temporelles.
    - process_digits(text) : sépare les chiffres des lettres et remplace les chiffres par 'digit'.

Fonctions :
- preprocess_query(query) : prétraite une requête utilisateur.
- process_and_merge_json(data, max_df) :
    - Fusionne les sections d’une étude en un seul texte, --> Plusieurs textes par étude et par section
    - Applique le nettoyage et le filtrage fréquentiel,
    - Retourne une liste de `Document` LangChain utilisables dans la recherche TF-IDF,
    - Sauvegarde également les résultats dans un JSON pour inspection.
"""

import os
import re
import json
import unicodedata
from nltk.corpus import stopwords
from nltk import word_tokenize, pos_tag
from nltk.stem import WordNetLemmatizer
from langchain.schema import Document

# nltk.download('punkt')
# nltk.download('averaged_perceptron_tagger')
# nltk.download('wordnet')
# nltk.download('stopwords')

from config.paths import SPARSE_JSON_PATH, SECTIONS_JSON_PATH, ACRONYMS_FILE

stop_words = set(stopwords.words('english'))

def get_wordnet_pos(treebank_tag):
    if treebank_tag.startswith('J'):
        return 'a'
    elif treebank_tag.startswith('V'):
        return 'v'
    elif treebank_tag.startswith('N'):
        return 'n'
    elif treebank_tag.startswith('R'):
        return 'r'
    else:
        return 'n'

def lemmatize_text(tokens):
    pos_tags = pos_tag(tokens)
    lemmatizer = WordNetLemmatizer()
    return [lemmatizer.lemmatize(token, get_wordnet_pos(pos)) for token, pos in pos_tags]

def replace_acronyms(acronyms_all, study_id, text):
    def replace_all_variants(text, acronym, definition):
        variants = {acronym, acronym.upper(), acronym.lower()}
        for variant in variants:
            text = re.sub(r'\(' + re.escape(variant) + r'\)', ' ', text)
            pattern = r'(?<!\w)' + re.escape(variant) + r'(?!\w)'
            text = re.sub(pattern, f' {definition.lower()} ', text)
        return text

    acronyms_study = acronyms_all.get(study_id, {})
    for acronym, definition in acronyms_study.items():
        text = replace_all_variants(text, acronym, definition)
    return text

def preprocess(text, study_id, acronyms_all):
    text = replace_acronyms(acronyms_all, study_id, text)
    words = word_tokenize(text)
    words = lemmatize_text(words)
    text = ' '.join(words)

    text = text.lower()

    text = unicodedata.normalize('NFKD', text).encode('ASCII', 'ignore').decode('utf-8')
    text = re.sub(r'[^\w\s+-]|_', ' ', text)
    text = text.replace("-", "")
    text = re.sub(r'\s+', ' ', text).strip()

    text = re.sub(r'\bd(\d+)\b', r'day \1', text)
    text = re.sub(r'\bw(\d+)\b', r'week \1', text)
    text = re.sub(r'\bm(\d+)\b', r'month \1', text)

    words = word_tokenize(text)
    words = [word for word in words if word not in stop_words and len(word) >= 2]

    return ' '.join(words)

def process_and_merge_sections(input_path=SECTIONS_JSON_PATH, acronyms_path=ACRONYMS_FILE, output_path=SPARSE_JSON_PATH ):
    with open(acronyms_path, 'r', encoding='utf-8') as f:
        acronyms_all = json.load(f)

    with open(input_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    processed_data = {}

    for study_id, sections in data.items():
        if not isinstance(sections, dict):
            print(f"[WARN] Étude {study_id} ignorée (sections non valides).")
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

def process_and_merge_json(existing=False):
    """
    Transforme les textes sectionnés et nettoyés en une liste de Documents LangChain.
    Chaque Document contient le texte d'une étude, sections conservées avec leurs noms.
    """
    if not(existing):
        data = process_and_merge_sections()

    else :
        with open(SPARSE_JSON_PATH, 'r', encoding='utf-8') as f:
            data = json.load(f)
    
    documents = []

    for study_id, sections in data.items():
        if not isinstance(sections, dict):
            print(f"[WARN] Étude {study_id} ignorée (sections non valides).")
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

def preprocess_query(query):
    study_id = "OPTISAGE"
    with open(ACRONYMS_FILE, 'r', encoding='utf-8') as f:
        acronyms_all = json.load(f)
    query_cleaned = preprocess(query, study_id, acronyms_all)
    return query_cleaned


# def process_and_merge_by_section(existing=False):
#     """
#     Transforme les textes nettoyés en une liste de Documents LangChain,
#     un Document par section (toutes études confondues), avec metadata 'section'.
#     """
#     if not(existing):
#         data = process_and_merge_sections()
#     else:
#         with open(SPARSE_JSON_PATH, 'r', encoding='utf-8') as f:
#             data = json.load(f)

#     section_groups = {}

#     for study_id, sections in data.items():
#         if not isinstance(sections, dict):
#             print(f"[WARN] Étude {study_id} ignorée (sections non valides).")
#             continue

#         for section_name, content in sections.items():
#             if section_name not in section_groups:
#                 section_groups[section_name] = []
#             section_groups[section_name].append(content)

#     documents = []
#     for section_name, contents in section_groups.items():
#         full_text = " ".join(contents).strip()
#         documents.append(Document(
#             page_content=full_text,
#             metadata={"section": section_name}
#         ))

#     print(f"Documents par section générés : {len(documents)}")
#     return documents
