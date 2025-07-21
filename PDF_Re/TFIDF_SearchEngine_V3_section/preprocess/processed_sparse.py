import re
import json
import unicodedata
from nltk.corpus import stopwords
from nltk import word_tokenize, pos_tag
from nltk.stem import WordNetLemmatizer
from config.paths import ACRONYMS_FILE_UNIQUE

# nltk.download('punkt')
# nltk.download('averaged_perceptron_tagger')
# nltk.download('wordnet')
# nltk.download('stopwords')


stop_words = set(stopwords.words('english'))

#TODO Changer year et old pour garder les ages
words_dont = ["be", "day", "week", "month", 'year', 'old', "kg", "ml", "g", "mg", "ph", "ng", "cm", "mm", "nm", "min", "cal", "kcal", "ppm", "ppb", "mm2", "mm3"]
roman_to_arabic = {
    "i": "1", "ii": "2", "iii": "3", "iv": "4",
    "v": "5", "vi": "6", "vii": "7", "viii": "8", "ix": "9"
}
acronym_generaux = {"vs" : "versus"}


def get_wordnet_pos(treebank_tag):
    if treebank_tag.startswith('J'):
        return 'a'
    elif treebank_tag.startswith('V'):
        return 'v'
    elif treebank_tag.startswith('N'):
        return 'n'
    elif treebank_tag.startswith('R'):
        return 'r'
    return 'n'

def lemmatize_text(tokens):
    pos_tags = pos_tag(tokens)
    lemmatizer = WordNetLemmatizer()
    return [lemmatizer.lemmatize(token, get_wordnet_pos(pos)) for token, pos in pos_tags]

def replace_all_variants(text, acronym, definition):
    variants = {acronym, acronym.upper(), acronym.lower()}
    for variant in variants:
        text = re.sub(r'\(' + re.escape(variant) + r'\)', ' ', text)
        pattern = r'(?<!\w)' + re.escape(variant) + r'(?!\w)'
        text = re.sub(pattern, f' {definition.lower()} ', text)
    return text

def replace_acronyms(acronyms_all, study_id, text):
    acronyms_study = acronyms_all.get(study_id, {})
    for acronym, definition in acronyms_study.items():
        text = replace_all_variants(text, acronym, definition)
    return text

def replace_roman_phrases(text):
    def convert_range(match):
        base = match.group(1)
        first = match.group(2)
        second = match.group(4)
        first = roman_to_arabic.get(first.lower(), first)
        second = roman_to_arabic.get(second.lower(), second)
        return f"{base}{first}{second}"

    def convert_single(match):
        base = match.group(1)
        numeral = match.group(2)
        numeral = roman_to_arabic.get(numeral.lower(), numeral)
        return f"{base}{numeral}"

    base_words = r"(?:phase|type|grade|types|phases|grades)"
    roman_or_digit = r"(?:ix|viii|vii|vi|iv|iii|ii|i|\d+)"

    pattern_range = re.compile(
        rf"\b({base_words})\s+({roman_or_digit})\s*([/-])\s*({roman_or_digit})\b",
        flags=re.IGNORECASE
    )
    text = pattern_range.sub(convert_range, text)

    pattern_single = re.compile(
        rf"\b({base_words})\s+({roman_or_digit})\b",
        flags=re.IGNORECASE
    )
    text = pattern_single.sub(convert_single, text)

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
    text = unicodedata.normalize('NFKD', text).encode('ASCII', 'ignore').decode('utf-8')
    
    for acro, defi in acronym_generaux.items():
        text = re.sub(rf'\b{acro}\b', f' {defi} ', text)
    
    if isQuery:
        text = replace_acronyms_query(acronyms_all, text)
    else: 
        text = replace_acronyms(acronyms_all, study_id, text)

    words = word_tokenize(text)
    words = lemmatize_text(words)
    text = ' '.join(words)

    text = text.lower()

    text = re.sub(r'[^\w\s-]|_', ' ', text)
    text = text.replace("-", "")
    text = re.sub(r'\s+', ' ', text).strip()

    text = replace_roman_phrases(text)

    tokens = word_tokenize(text)
    tokens = [w for w in tokens if (w not in stop_words or w.isdigit()) and (len(w) > 1 or w.isdigit())]
    text = ' '.join(tokens)

    text = re.sub(r'\bd(\d+)\b', " ", text)
    text = re.sub(r'\bw(\d+)\b', " ", text)
    text = re.sub(r'\bm(\d+)\b', " ", text)
    text = re.sub(r'\b\d+\b', " ", text)
    text = re.sub(r'\b\d+x\d+\b', ' ', text)


    tokens = word_tokenize(text)
    unit_pattern = re.compile(rf"^\d+(\.\d+)?({'|'.join(re.escape(u) for u in words_dont)})$", re.IGNORECASE)
    tokens = [w for w in tokens if w not in words_dont and not unit_pattern.match(w)]

    return ' '.join(tokens)


def preprocess_query(query):
    study_id = None
    with open(ACRONYMS_FILE_UNIQUE, 'r', encoding='utf-8') as f:
        acronyms_all_unique = json.load(f)
    query_cleaned = preprocess(query, study_id, acronyms_all_unique, isQuery=True)
    # print(query_cleaned)
    return query_cleaned