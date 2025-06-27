import json
import re
import unicodedata
from nltk.corpus import stopwords
from nltk import word_tokenize, pos_tag
from nltk.stem import WordNetLemmatizer
import os

# Chargement des acronymes
ACRONYMS_FILE = "/home/loris/Stage/STAGE/Test/PDF_RE/TFIDF_SearchEngine_V2/data/extracted_acronym_final.json"
with open(ACRONYMS_FILE, "r", encoding="utf-8") as f:
    acronyms_all = json.load(f)

# Stopwords
stop_words = set(stopwords.words('english'))

# Fonctions NLP
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

# Fonction de prétraitement
def preprocess(text, study_id):
    text = replace_acronyms(acronyms_all, study_id, text)

    words = word_tokenize(text)
    words = lemmatize_text(words)
    text = ' '.join(words)

    text = unicodedata.normalize('NFKD', text).encode('ASCII', 'ignore').decode('utf-8')
    text = text.lower()
    text = re.sub(r'[^\w\s+-]|_', ' ', text)
    text = text.replace("-", "")

    text = re.sub(r'\bd(\d+)\b', " ", text)
    text = re.sub(r'\bw(\d+)\b', " ", text)
    text = re.sub(r'\bm(\d+)\b', " ", text)
    text = re.sub(r'\b\d+\b', " ", text)

    words = word_tokenize(text)
    words = [word for word in words if word not in stop_words and len(word) >= 2]
    final_text = ' '.join(words)

    return final_text

# Lecture des sections
INPUT_FILE = "/home/loris/Stage/STAGE/Test/PDF_RE/TFIDF_SearchEngine_V2/data/sections_sorted.json"
with open(INPUT_FILE, 'r', encoding='utf-8') as f:
    text_data = json.load(f)

# Structure du résultat
output_data = {}

# Prétraitement
for study_id, sections in text_data.items():
    output_data[study_id] = {}
    for section_title, entries in sections.items():
        merged_text = ' '.join(entries)
        processed_text = preprocess(merged_text, study_id)
        output_data[study_id][section_title] = processed_text

# Sauvegarde du JSON
OUTPUT_FILE = "/home/loris/Stage/STAGE/Test/PDF_RE/Preprocess/Preprocess_explain_full.json"
with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
    json.dump(output_data, f, indent=2, ensure_ascii=False)

print(f"Fichier sauvegardé dans : {OUTPUT_FILE}")
