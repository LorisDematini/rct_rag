import json
import re
import unicodedata
from nltk.corpus import stopwords
from nltk import word_tokenize, pos_tag
from nltk.stem import WordNetLemmatizer

# nltk.download('punkt')
# nltk.download('averaged_perceptron_tagger')
# nltk.download('wordnet')
# nltk.download('stopwords')

stop_words = set(stopwords.words('english'))

acronyms_file = "/home/loris/Stage/STAGE/Test/PDF_RE/Acronym/final_acronyms.json"
acronyms_file_specific = "/home/loris/Stage/STAGE/Test/PDF_RE/Acronym/acronym_extracted.json"

# Fonction de mapping POS
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

# Fonction de lemmatisation
def lemmatize_text(tokens):
    lemmatizer = WordNetLemmatizer()
    pos_tags = pos_tag(tokens)

    lemmatized_tokens = []
    for token, pos in pos_tags:
        wordnet_pos = get_wordnet_pos(pos)
        lemma = lemmatizer.lemmatize(token, wordnet_pos)
        lemmatized_tokens.append(lemma)

    return lemmatized_tokens

#Fonction pour remplacer les acronym en commençant par les spécifiques
def replace_acronyms(acronyms_global, acronyms_specific_all, study_id, text):
    acronyms_study_specific = acronyms_specific_all.get(study_id, {})

    for acronym, definition in acronyms_study_specific.items():
        if isinstance(definition, str):
            pattern_parentheses = r'\(' + re.escape(acronym) + r'\)'
            text = re.sub(pattern_parentheses, '', text, flags=re.IGNORECASE)

            pattern = r'(?<![\w(])' + re.escape(acronym) + r'(?![\w)])'
            text = re.sub(pattern, definition.lower(), text, flags=re.IGNORECASE)

    for acronym, definition in acronyms_global.items():
        if isinstance(definition, str):
            pattern_parentheses = r'\(' + re.escape(acronym) + r'\)'
            text = re.sub(pattern_parentheses, '', text, flags=re.IGNORECASE)

            pattern = r'(?<![\w(])' + re.escape(acronym) + r'(?![\w)])'
            text = re.sub(pattern, definition.lower(), text, flags=re.IGNORECASE)

    return text


#Fonction de Preprocess
def preprocess(text, study_id, acronyms_global, acronyms_specific_all):
    #1. Acronyme
    text = replace_acronyms(acronyms_global, acronyms_specific_all, study_id, text)

    #2. Lemmatisations
    words = word_tokenize(text)
    words = lemmatize_text(words)

    text = ' '.join(words)

    # 3. Normalisation Unicode → ASCII
    text = unicodedata.normalize('NFKD', text).encode('ASCII', 'ignore').decode('utf-8')

    # 4. Nettoyage ponctuation
    text = re.sub(r'[^\w\s+-]|_', ' ', text)
    text = text.replace("-", "")
    text = re.sub(r'\s+', ' ', text).strip()

    # 5. Minuscules
    text = text.lower()

    # 6. Normalisation d1, w2, m3 → day/week/month
    text = re.sub(r'\bd(\d+)\b', r'day \1', text)
    text = re.sub(r'\bw(\d+)\b', r'week \1', text)
    text = re.sub(r'\bm(\d+)\b', r'month \1', text)
    
    words = word_tokenize(text)
    # 7. Tokenisation par mots + suppression stopwords
    # + Nombres et chiffres : and not any(char.isdigit() for char in word)
    words = [word for word in words if word not in stop_words and len(word) >= 2]

    return ' '.join(words)

# Chargement fichiers JSON
with open(acronyms_file, 'r', encoding='utf-8') as f:
    acronyms_global = json.load(f)

with open(acronyms_file_specific, 'r', encoding='utf-8') as f1:
    acronyms_specific_all = json.load(f1)

with open("/home/loris/Stage/STAGE/Test/PDF_RE/Sections/sections_sorted.json", "r", encoding="utf-8") as f2:
    data = json.load(f2)

    for study_id in list(data.keys()):
        if "OTHER" in data[study_id]:
            del data[study_id]["OTHER"]

# Application de preprocess à chaque section en les fusionnant
for study_id, sections in data.items():
    for section_title, entries in sections.items():
        cleaned_entries = [entry.split(':', 1)[1].strip() for entry in entries]
        full_text = ' '.join(cleaned_entries)
        data[study_id][section_title] = preprocess(full_text, study_id, acronyms_global, acronyms_specific_all)

# Sauvegarde
with open("/home/loris/Stage/STAGE/Test/PDF_RE/Preprocess/sections_preprocessed_lemma.json", "w", encoding="utf-8") as f3:
    json.dump(data, f3, indent=2, ensure_ascii=False)
