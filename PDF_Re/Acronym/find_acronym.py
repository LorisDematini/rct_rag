import re
import json

def extract_acronyms(text):
    acronyms = set()

    # Acronymes en majuscules
    acronyms.update(re.findall(r'\b[A-Z]{2,6}\b', text))


    # mixed = re.findall(r'\b\w*[A-Z]\w*[A-Z]\b', text)
    # acronyms.update(mixed)

    return sorted(acronyms)

with open("/home/loris/Stage/STAGE/Test/PDF_RE/Preprocess/sections_preprocessed_lemma.json", "r", encoding="utf-8") as f:
    data = json.load(f)

all_text = ""
for study in data.values():
    all_text += " ".join(str(value) for value in study.values()) + " "

acronyms_found = extract_acronyms(all_text)
print(len(acronyms_found))
print(acronyms_found)
