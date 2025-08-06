import re
import unicodedata
import nltk
nltk.data.path.append("/usr/share/nltk_data")
from nltk.corpus import stopwords
from nltk import word_tokenize, pos_tag
from nltk.tokenize import sent_tokenize
from nltk.stem import WordNetLemmatizer
from typing import List, Tuple, Dict

# nltk.download('punkt')
# nltk.download('averaged_perceptron_tagger')
# nltk.download('wordnet')
# nltk.download('stopwords')

stop_words = set(stopwords.words('english'))

words_dont = ["be", "day", "week", "month", 'year', 'old', "kg", "ml", "g", "mg", "ph", "ng", "cm", "mm", "nm", "min", "cal", "kcal", "ppm", "ppb", "mm2", "mm3"]

roman_to_arabic = {
    "i": "1", "ii": "2", "iii": "3", "iv": "4",
    "v": "5", "vi": "6", "vii": "7", "viii": "8", "ix": "9"
}

acronym_generaux = {"vs": "versus"}


def get_wordnet_pos(treebank_tag: str) -> str:
    """
    Maps Treebank POS tags to WordNet POS tags for lemmatization.
    """
    if treebank_tag.startswith('J'):
        return 'a'  # adjective
    elif treebank_tag.startswith('V'):
        return 'v'  # verb
    elif treebank_tag.startswith('N'):
        return 'n'  # noun
    elif treebank_tag.startswith('R'):
        return 'r'  # adverb
    return 'n'  # default to noun


def lemmatize_text(tokens: List[str]) -> List[str]:
    """
    Lemmatizes a list of tokens using their POS tags.
    """
    pos_tags: List[Tuple[str, str]] = pos_tag(tokens)
    lemmatizer = WordNetLemmatizer()
    return [lemmatizer.lemmatize(token, get_wordnet_pos(pos)) for token, pos in pos_tags]


def replace_all_variants(text: str, acronym: str, definition: str) -> str:
    """
    Replaces all case variants of an acronym in the text with its definition.
    Also removes the acronym if it's between parentheses.
    """
    variants = {acronym, acronym.upper(), acronym.lower()}
    for variant in variants:
        # Remove parenthesized acronym
        text = re.sub(r'\(' + re.escape(variant) + r'\)', ' ', text)
        # Replace standalone variant
        pattern = r'(?<!\w)' + re.escape(variant) + r'(?!\w)'
        text = re.sub(pattern, f' {definition.lower()} ', text)
    return text


def replace_acronyms(acronyms_all: Dict[str, Dict[str, str]], study_id: str, text: str) -> str:
    """
    Replaces all acronyms found in the study with their definitions in the given text.
    """
    acronyms_study = acronyms_all.get(study_id, {})
    for acronym, definition in acronyms_study.items():
        text = replace_all_variants(text, acronym, definition)
    return text


def replace_roman_phrases(text: str) -> str:
    """
    Converts phrases like 'Grade IV' to numeric equivalents (Grade4).
    Handles both single and ranged Roman numerals.
    """
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


def preprocess(text: str, study_id: str, acronyms_all: Dict[str, Dict[str, str]]) -> str:
    """
    Full preprocessing pipeline for a single study text:
    - Normalize unicode
    - Replace general and study-specific acronyms
    - Tokenize and lemmatize
    - Remove punctuation, digits, stopwords and unwanted units
    - Normalize Roman numeral expressions
    - Final cleanup and filtering
    """
    # Normalize unicode characters
    text = unicodedata.normalize('NFKD', text).encode('ASCII', 'ignore').decode('utf-8')
    
    # Replace general acronyms
    for acro, defi in acronym_generaux.items():
        text = re.sub(rf'\b{acro}\b', f' {defi} ', text)
    
    # Replace study-specific acronyms
    text = replace_acronyms(acronyms_all, study_id, text)

    # Tokenize sentences and words
    sentences = sent_tokenize(text, language="english")
    words = [word for sent in sentences for word in word_tokenize(sent)]

    # Lemmatization
    words = lemmatize_text(words)

    # Lowercase and remove punctuation
    text = ' '.join(words)
    text = text.lower()
    text = re.sub(r'[^\w\s-]|_', ' ', text)
    text = text.replace("-", "")
    text = re.sub(r'\s+', ' ', text).strip()

    # Replace Roman numeral expressions
    text = replace_roman_phrases(text)

    # Tokenize again and remove stopwords and short words
    tokens = [word for sent in sent_tokenize(text, language="english") for word in word_tokenize(sent)]
    tokens = [w for w in tokens if (w not in stop_words or w.isdigit()) and (len(w) > 1 or w.isdigit())]

    # Join tokens into final text
    text = ' '.join(tokens)

    # Remove time or quantity expressions (e.g., d14, w2, m6, etc.)
    text = re.sub(r'\bd(\d+)\b', " ", text)
    text = re.sub(r'\bw(\d+)\b', " ", text)
    text = re.sub(r'\bm(\d+)\b', " ", text)
    text = re.sub(r'\b\d+\b', " ", text)
    text = re.sub(r'\b\d+x\d+\b', ' ', text)

    # Remove measurement units like 10mg, 3ml, etc.
    tokens = word_tokenize(text)
    unit_pattern = re.compile(rf"^\d+(\.\d+)?({'|'.join(re.escape(u) for u in words_dont)})$", re.IGNORECASE)
    tokens = [w for w in tokens if w not in words_dont and not unit_pattern.match(w)]

    return ' '.join(tokens)