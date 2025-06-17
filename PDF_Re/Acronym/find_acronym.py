import re
import json

def extract_acronyms(text):
    acronyms = set()
    # full_maj = re.findall(r'\b[A-Z]{2,}\b', text)
    mixed = re.findall(r'\b\w*[A-Z]\w*[A-Z]\b', text)
    acronyms.update(mixed)
    return sorted(acronyms)

def simplify_title(title):
    title = title.upper()
    title = re.sub(r'[-/\s]', ' ', title)
    title = re.sub(r'\d+', ' ', title)

    return title.split()[0]

with open("/home/loris/Stage/STAGE/Test/PDF_RE/Preprocess/sections_preprocessed_lemma.json", "r", encoding="utf-8") as f:
    data = json.load(f)

title_prefixes = set()
for study_id, study in data.items():
    title_section = study_id
    simplified = simplify_title(title_section)
    if simplified :
        title_prefixes.add(simplified)

all_text = " ".join(" ".join(str(value) for value in study.values()) for study in data.values())
acronyms_found = extract_acronyms(all_text)

filtered_acronyms = []
for acro in acronyms_found:
    acro_upper = acro.upper()
    keep = True
    for prefix in title_prefixes:
        if acro_upper == prefix or acro_upper.startswith(prefix):
            keep = False
            break
#On peut delete len(acro) < 7
    if keep and len(acro) < 7:
        filtered_acronyms.append(acro)
acronyms_bizarre = []

for acro in filtered_acronyms[:]:
    has_digit = any(char.isdigit() for char in acro)
    lower_count = sum(1 for char in acro if char.islower())

    if has_digit or lower_count >= 2:
        acronyms_bizarre.append(acro)
        filtered_acronyms.remove(acro)

print(f"\n{len(filtered_acronyms)} acronymes valides après nettoyage :")
print(filtered_acronyms)

print(f"\n{len(acronyms_bizarre)} acronymes bizarres :")
print(acronyms_bizarre)

filtered_acronyms.extend(acronyms_bizarre)
acronym_dict = {acro: "" for acro in filtered_acronyms}

with open("/home/loris/Stage/STAGE/Test/PDF_RE/Acronym/acronym_nonTrouve.json", "w", encoding="utf-8") as f:
    json.dump(acronym_dict, f, ensure_ascii=False, indent=2)