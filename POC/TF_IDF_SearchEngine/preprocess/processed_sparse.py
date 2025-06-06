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
    - Fusionne les sections d’une étude en un seul texte,
    - Applique le nettoyage et le filtrage fréquentiel,
    - Retourne une liste de `Document` LangChain utilisables dans la recherche TF-IDF,
    - Sauvegarde également les résultats dans un JSON pour inspection.
"""


import re
import unicodedata
import json
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import nltk
from config.paths import ACRONYMS_FILE, SPARSE_JSON_PATH
from langchain.schema import Document
from collections import defaultdict

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

def process_and_merge_json(input_data, max_df=0.95):
    preprocessor = TextPreprocessor()
    raw_documents = []
    doc_freq = defaultdict(int)

    # 1. Prétraitement initial sans filtrage
    for study_id, sections in input_data.items():
        if not isinstance(sections, list):
            print(f"[WARN] Étude {study_id} ignorée (sections non valides).")
            continue

        full_text = []
        for pair in sections:
            if isinstance(pair, list) and len(pair) == 2:
                _, section_content = pair
                if isinstance(section_content, str):
                    text = preprocessor.normalize_text(section_content)
                    text = preprocessor.replace_acronyms(text)
                    text = preprocessor.replace_special_terms(text)
                    full_text.append(text)

        if full_text:
            merged_text = ' '.join(full_text)
            raw_documents.append((study_id, merged_text))

            # Compter les mots uniques de ce document
            unique_words = set(merged_text.split())
            for word in unique_words:
                doc_freq[word] += 1

    num_docs = len(raw_documents)
    max_doc_thresh = num_docs * max_df
    to_filter = {word for word, freq in doc_freq.items() if freq >= max_doc_thresh}

    print(f"[INFO] Nombre de mots filtrés (présents dans ≥ {max_df*100:.0f}% des documents) : {len(to_filter)}")
    # Affiche tous les mots filtrés
    print(f"[INFO] Liste des mots filtrés : {list(to_filter)}")

    # 2. Retraitement en supprimant les mots filtrés
    final_documents = []
    merged_dict = {}

    for study_id, text in raw_documents:
        words = [word for word in text.split() if word not in to_filter]
        filtered_text = ' '.join(words)

        final_documents.append(Document(
            page_content=filtered_text,
            metadata={"study_id": study_id}
        ))
        merged_dict[study_id] = filtered_text

    # 3. Sauvegarde
    with open(SPARSE_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(merged_dict, f, ensure_ascii=False, indent=2)

    print(f"[INFO] Études traitées : {len(final_documents)}")
    print(f"[INFO] JSON fusionné enregistré dans : {SPARSE_JSON_PATH}")

    return final_documents



