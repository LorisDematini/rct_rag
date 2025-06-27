import json
import re
import unicodedata
from nltk.corpus import stopwords
from nltk import word_tokenize, pos_tag
from nltk.stem import WordNetLemmatizer
import os

ACRONYMS_FILE = "/home/loris/Stage/STAGE/Test/PDF_RE/TFIDF_SearchEngine_V2/data/extracted_acronym_final.json"
with open(ACRONYMS_FILE, "r", encoding="utf-8") as f:
    acronyms_all = json.load(f)

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
    print(tokens, pos_tags)
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

def preprocess(text, study_id, acronyms_all, output_file):
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n[TEXTE DE BASE]\n")
        f.write(text + "\n")

        text = replace_acronyms(acronyms_all, study_id, text)
        f.write("\n[APRÈS REMPLACEMENT ACRONYMES]\n")
        f.write(text + "\n")

        words = word_tokenize(text)
        words = lemmatize_text(words)
        text = ' '.join(words)
        f.write("\n[APRÈS LEMMATISATION]\n")
        f.write(text + "\n")

        text = unicodedata.normalize('NFKD', text).encode('ASCII', 'ignore').decode('utf-8')
        f.write("\n[NORMALISATION UTF-8]\n")
        f.write(text + "\n")

        text = text.lower()
        f.write("\n[EN MINUSCULES]\n")
        f.write(text + "\n")

        text = re.sub(r'[^\w\s+-]|_', ' ', text)
        text = text.replace("-", "")
        f.write("\n[REMPLACEMENT PONCTUATION]\n")
        f.write(text + "\n")

        text = re.sub(r'\bd(\d+)\b', " ", text)
        text = re.sub(r'\bw(\d+)\b', " ", text)
        text = re.sub(r'\bm(\d+)\b', " ", text)
        f.write("\n[SUPPRESSION D/W/M + CHIFFRES]\n")
        f.write(text + "\n")

        text = re.sub(r'\b\d+\b', " ", text)
        f.write("\n[SUPPRESSION CHIFFRES ISOLES]\n")
        f.write(text + "\n")

        words = word_tokenize(text)
        words = [word for word in words if word not in stop_words and len(word) >= 2]
        final_text = ' '.join(words)
        f.write("\n[SUPPRESSION STOPWORDS ET MOTS COURTS]\n")
        f.write(final_text + "\n")

    return final_text

text = {
    "RUBI": {
        "TITLE": [
            "The study's evaluated the effects of Good Clinical Practice (GCP) in ICH of ps2 treatment d10 ≥ 12 — which, m3 surprisingly,\nimproved patients-outcomes."
        ]
    }
}

for study_id, sections in text.items():
    for section_title, entries in sections.items():
        merged_text = ' '.join(entries)
        output_txt_path = f"/home/loris/Stage/STAGE/Test/PDF_RE/Preprocess/Preprocess_explain.txt"
        processed_text = preprocess(merged_text, study_id, acronyms_all, output_txt_path)
        print(f"Texte prétraité enregistré dans : {output_txt_path}")
