import json
import re
import unicodedata
from nltk.corpus import stopwords


stop_words = set(stopwords.words('english'))
acronyms_file = "/home/loris/Stage/STAGE/Test/PDF_RE/Acronym/final_acronyms.json"
acronyms_file_specific = "/home/loris/Stage/STAGE/Test/PDF_RE/acronym_extracted.json"

def replace_acronyms(acronyms_global, acronyms_specific_all, study_id, text):
    acronyms_study_specific = acronyms_specific_all.get(study_id, {})

    for acronym, definition in acronyms_study_specific.items():
        if isinstance(definition, str):
            pattern = r'(?<![\w-])' + re.escape(acronym) + r'(?![\w-])'
            text = re.sub(pattern, definition.lower(), text, flags=re.IGNORECASE)

    for acronym, definition in acronyms_global.items():
        if isinstance(definition, str):
            pattern = r'(?<![\w-])' + re.escape(acronym) + r'(?![\w-])'
            text = re.sub(pattern, definition.lower(), text, flags=re.IGNORECASE)

    return text


def preprocess(text, study_id, acronyms_global, acronyms_specific_all):
    text = replace_acronyms(acronyms_global, acronyms_specific_all, study_id, text)
    
    #2. utf-8 : Sans accent/cédille/signe bizarre
    text = unicodedata.normalize('NFKD', text).encode('ASCII', 'ignore').decode('utf-8')

    #3. Retire tout ponctuation
    text = re.sub(r'[^\w\s+-]|_', ' ', text)
    text = text.replace("-", "")
    #Espace en trop
    text = re.sub(r'\s+', ' ', text).strip()

    #print("DEBUT : ",text)
    #4. Minusculise le texte
    text = text.lower()

    # Remplace d+chiffre par "day chiffre"
    text = re.sub(r'\bd(\d+)\b', r'day \1', text)
    # Remplace w+chiffre par "week chiffre"
    text = re.sub(r'\bw(\d+)\b', r'week \1', text)
    # Remplace m+chiffre par "month chiffre"
    text = re.sub(r'\bm(\d+)\b', r'month \1', text)
    
    
    #Stopwords
    words = text.split()
    words = [word for word in words if word not in stop_words and len(word)>=2]
    text = ' '.join(words)

    return text

with open(acronyms_file, 'r', encoding='utf-8') as f:
    acronyms_global = json.load(f)

with open(acronyms_file_specific, 'r', encoding='utf-8') as f1:
    acronyms_specific_all = json.load(f1)

with open("/home/loris/Stage/STAGE/Test/PDF_RE/Sections/sections_sorted.json", "r", encoding="utf-8") as f3:
    data = json.load(f3)

    for study_id in list(data.keys()):
        if "OTHER" in data[study_id]:
            del data[study_id]["OTHER"]

for study_id, sections in data.items():
    for section_title, entries in sections.items():
        cleaned_entries = [entry.split(':', 1)[1].strip() for entry in entries]
        full_text = ' '.join(cleaned_entries)
        data[study_id][section_title] = preprocess(full_text, study_id, acronyms_global, acronyms_specific_all)


with open("/home/loris/Stage/STAGE/Test/PDF_RE/Preprocess/sections_preprocessed.json", "w", encoding="utf-8") as f4:
    json.dump(data, f4, indent=2, ensure_ascii=False)

