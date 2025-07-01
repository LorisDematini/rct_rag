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

from config.paths import ACRONYMS_FILE_UNIQUE, SPARSE_JSON_PATH, SECTIONS_JSON_PATH, ACRONYMS_FILE

stop_words = set(stopwords.words('english'))
words_dont = ["be", "day", "week", "month", "year","kg", "ml", "g", "mg", "ng", "cm", "mm", "nm", "min", "cal", "kcal", "ppm", "ppb", "mm2", "mm3"]
roman_to_arabic = {"i": "1","ii": "2","iii": "3","iv": "4","v": "5","vi": "6","vii": "7","viii": "8","ix": "9"}


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


def replace_acronyms_query(acronyms_all, text):
    # dictionnaire en minuscule
    acronyms_all_lower = {k.lower(): v for k, v in acronyms_all.items()}

    def replace_match(match):
        token = match.group(0)
        token_lower = token.lower()
        definition = acronyms_all_lower.get(token_lower)
        if definition:
            return f"{definition.lower()} {token_lower}"
        else:
            return token

    pattern = r'\b[a-zA-Z]{2,}\b'
    return re.sub(pattern, replace_match, text)



def preprocess(text, study_id, acronyms_all, isQuery=False):
    if isQuery:
        text = replace_acronyms_query(acronyms_all, text)
    else: 
        text = replace_acronyms(acronyms_all, study_id, text)
    words = word_tokenize(text)
    words = lemmatize_text(words)
    text = ' '.join(words)

    text = unicodedata.normalize('NFKD', text).encode('ASCII', 'ignore').decode('utf-8')
    text = text.lower()

    text = re.sub(r'[^\w\s+-]|_', ' ', text)
    text = text.replace("-", "")
    text = re.sub(r'\s+', ' ', text).strip()

    text = re.sub(r'[^\w\s+-]|_', ' ', text)
    text = text.replace("-", "")

    text = re.sub(r'\bd(\d+)\b', " ", text)
    text = re.sub(r'\bw(\d+)\b', " ", text)
    text = re.sub(r'\bm(\d+)\b', " ", text)
    text = re.sub(r'\b\d+\b', " ", text)

    for roman, arabic in sorted(roman_to_arabic.items(), key=lambda x: -len(x[0])):
        text = re.sub(rf'\b{roman}\b', f' {arabic} ', text)

    words = word_tokenize(text)
    words = [
        word for word in words
        if (word not in stop_words or word.isdigit()) and (len(word) > 1 or word.isdigit())
    ]

    # regex pour détecter nombre + unité comme 30mg
    unit_pattern = re.compile(rf"^\d+(\.\d+)?({'|'.join(re.escape(u) for u in words_dont)})$", re.IGNORECASE)

    words = [
        word for word in words
        if word not in words_dont and not unit_pattern.match(word)
    ]

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
    study_id = None
    with open(ACRONYMS_FILE_UNIQUE, 'r', encoding='utf-8') as f:
        acronyms_all_unique = json.load(f)
    query_cleaned = preprocess(query, study_id, acronyms_all_unique, isQuery=True)
    return query_cleaned