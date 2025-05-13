import re
import unicodedata
import json
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import nltk
from config.paths import ACRONYMS_FILE

# Télécharger les ressources nécessaires
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('omw-1.4')


class TextPreprocessor:
    def __init__(self, acronyms_file=ACRONYMS_FILE):
        self.acronyms_file = acronyms_file
        self.stop_words = set(stopwords.words('english')).union({
            'patient', 'patients', 'study', 'studies', 'treatment', 'trial', 'clinical'
        })
        self.lemmatizer = WordNetLemmatizer()

        with open(acronyms_file, 'r', encoding='utf-8') as f:
            self.acronyms = json.load(f)

    def process_digits(self, text):
        text = re.sub(r'(\d+)([a-zA-Z]+)', r'\1 \2', text)
        text = re.sub(r'([a-zA-Z]+)(\d+)', r'\1 \2', text)
        text = re.sub(r'\b\d+\b', 'digit', text)
        text = re.sub(r'(digit\s+){2,}', 'digit ', text)
        return text.strip()

    def lemmatize_words(self, words):
        return [self.lemmatizer.lemmatize(word) for word in words]

    def normalize_text(self, text):
        if not isinstance(text, str):
            return ""

        text = text.lower()
        text = unicodedata.normalize('NFKD', text).encode('ASCII', 'ignore').decode('utf-8')
        text = re.sub(r'[^\w\s]', ' ', text)
        text = re.sub(r'\s+', ' ', text).strip()

        text = self.process_digits(text)

        words = text.split()
        words = [word for word in words if word not in self.stop_words]
        words = self.lemmatize_words(words)
        words = [word for word in words if len(word) > 1]
        return ' '.join(words)

    def replace_acronyms(self, text):
        for acronym, definition in self.acronyms.items():
            pattern = r'\b' + re.escape(acronym) + r'\b'
            text = re.sub(pattern, definition.lower(), text, flags=re.IGNORECASE)
        return text

    def replace_special_terms(self, text):
        text = re.sub(r'\bd(\d{1,2}|100)\b', r'day \1', text)
        text = re.sub(r'\bm(\d{1,2}|100)\b', r'month \1', text)
        text = re.sub(r'\bw(\d{1,2}|100)\b', r'week \1', text)
        return text

def preprocess_query(query):
    preprocessor = TextPreprocessor()

    query = preprocessor.normalize_text(query)
    query = preprocessor.replace_acronyms(query)
    query = preprocessor.replace_special_terms(query)
    return query

def process_and_merge_json(input_data):
    preprocessor = TextPreprocessor()
    merged_data = {}

    for study_id, sections in input_data.items():
        if not isinstance(sections, list):
            print(f"Étude {study_id} ignorée (sections non valides).")
            continue

        # Fusionner tout le contenu des sections en un seul texte par étude
        full_text = []
        for pair in sections:
            if isinstance(pair, list) and len(pair) == 2:
                section_title, section_content = pair
                if isinstance(section_content, str):
                    text = preprocessor.normalize_text(section_content)
                    text = preprocessor.replace_acronyms(text)
                    text = preprocessor.replace_special_terms(text)
                    full_text.append(text)

        if full_text:
            merged_data[study_id] = ' '.join(full_text)

    print(f"Nombre d'études fusionnées : {len(merged_data)}")
    return merged_data

