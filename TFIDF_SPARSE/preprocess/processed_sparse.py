import re
import json
import unicodedata
import nltk
nltk.data.path.append("/usr/share/nltk_data")

from nltk.corpus import stopwords
from nltk import word_tokenize, pos_tag
from nltk.tokenize import sent_tokenize
from nltk.stem import WordNetLemmatizer

from config.paths import ACRONYMS_FILE_UNIQUE

# NLTK setup
stop_words = set(stopwords.words('english'))

# Words/units to ignore even if not in stopwords
words_dont = ["be", "day", "week", "month", 'year', 'old', "kg", "ml", "g", "mg", "ph", 
              "ng", "cm", "mm", "nm", "min", "cal", "kcal", "ppm", "ppb", "mm2", "mm3"]

# Roman numerals mapping for conversion
roman_to_arabic = {
    "i": "1", "ii": "2", "iii": "3", "iv": "4",
    "v": "5", "vi": "6", "vii": "7", "viii": "8", "ix": "9"
}

# Generic acronyms to be replaced
acronym_generaux = {"vs": "versus"}


def get_wordnet_pos(treebank_tag):
    """Map NLTK POS tags to WordNet tags for better lemmatization."""
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
    """Apply POS-based lemmatization."""
    pos_tags = pos_tag(tokens)
    lemmatizer = WordNetLemmatizer()
    return [lemmatizer.lemmatize(token, get_wordnet_pos(pos)) for token, pos in pos_tags]


def replace_roman_phrases(text):
    """Replace roman numerals used in phases/types with numeric forms."""
    def convert_range(match):
        base, first, _, second = match.groups()
        return f"{base}{roman_to_arabic.get(first.lower(), first)}{roman_to_arabic.get(second.lower(), second)}"

    def convert_single(match):
        base, numeral = match.groups()
        return f"{base}{roman_to_arabic.get(numeral.lower(), numeral)}"

    base_words = r"(?:phase|type|grade|types|phases|grades)"
    roman_or_digit = r"(?:ix|viii|vii|vi|iv|iii|ii|i|\d+)"

    pattern_range = re.compile(rf"\b({base_words})\s+({roman_or_digit})\s*([/-])\s*({roman_or_digit})\b", re.IGNORECASE)
    pattern_single = re.compile(rf"\b({base_words})\s+({roman_or_digit})\b", re.IGNORECASE)

    text = pattern_range.sub(convert_range, text)
    text = pattern_single.sub(convert_single, text)

    return text


def replace_acronyms_query(acronyms_all, query):
    """Replace acronyms in the query with their definitions + acronym."""
    acronyms_all_lower = {k.lower(): v for k, v in acronyms_all.items()}

    def replace_match(match):
        token = match.group(0)
        definition = acronyms_all_lower.get(token.lower())
        return f"{definition.lower()} {token.lower()}" if definition else token

    return re.sub(r'\b[a-zA-Z]{2,}\b', replace_match, query)


def preprocess_query(text):
    """
    Preprocess user query for TF-IDF search:
    - Normalize unicode
    - Replace acronyms
    - Tokenize, lemmatize
    - Remove stopwords and measurement units
    - Replace roman numerals in certain contexts
    - Clean up numbers and punctuation
    """
    # Normalize Unicode (remove accents, etc.)
    text = unicodedata.normalize('NFKD', text).encode('ASCII', 'ignore').decode('utf-8')

    # Load acronym dictionary
    with open(ACRONYMS_FILE_UNIQUE, 'r', encoding='utf-8') as f:
        acronyms_all_unique = json.load(f)

    # Replace generic acronyms
    for acro, definition in acronym_generaux.items():
        text = re.sub(rf'\b{acro}\b', f' {definition} ', text)

    # Replace acronyms from file
    text = replace_acronyms_query(acronyms_all_unique, text)

    # Sentence tokenization and lemmatization
    sentences = sent_tokenize(text, language="english")
    words = [word for sent in sentences for word in word_tokenize(sent)]
    words = lemmatize_text(words)
    text = ' '.join(words)

    # Lowercase and remove punctuation
    text = text.lower()
    text = re.sub(r'[^\w\s-]|_', ' ', text)
    text = text.replace("-", "")
    text = re.sub(r'\s+', ' ', text).strip()

    # Replace Roman numerals in phrases (e.g., "Phase II" → "Phase2")
    text = replace_roman_phrases(text)

    # Token filtering: remove stopwords and short tokens
    tokens = [
        w for sent in sent_tokenize(text, language="english")
        for w in word_tokenize(sent)
        if (w not in stop_words or w.isdigit()) and (len(w) > 1 or w.isdigit())
    ]
    text = ' '.join(tokens)

    # Remove specific patterns: d12, w3, m4, etc.
    text = re.sub(r'\bd(\d+)\b', " ", text)
    text = re.sub(r'\bw(\d+)\b', " ", text)
    text = re.sub(r'\bm(\d+)\b', " ", text)

    # Remove standalone numbers and "NxM" patterns
    text = re.sub(r'\b\d+\b', " ", text)
    text = re.sub(r'\b\d+x\d+\b', ' ', text)

    # Final filter to remove unwanted measurement units
    tokens = word_tokenize(text)
    unit_pattern = re.compile(rf"^\d+(\.\d+)?({'|'.join(re.escape(u) for u in words_dont)})$", re.IGNORECASE)
    tokens = [w for w in tokens if w not in words_dont and not unit_pattern.match(w)]

    return ' '.join(tokens)
