import re
import json
import os

base_path = os.getcwd()

input_json = os.path.join(base_path, "Preprocess", "sections_preprocessed_lemma.json")
output_json = os.path.join(base_path, "Acronym", "acronym_nonTrouve_section.json")

def extract_acronyms(text):
    acronyms = set()
    mixed = re.findall(r'\b\w*[A-Z]\w*[A-Z]\b', text)
    acronyms.update(mixed)
    return sorted(acronyms)

def simplify_title(title):
    title = title.upper()
    title = re.sub(r'[-/\s]', ' ', title)
    title = re.sub(r'\d+', ' ', title)
    return title.split()[0]

with open(input_json, "r", encoding="utf-8") as f:
    data = json.load(f)

title_prefixes = set()
for study_id in data:
    simplified = simplify_title(study_id)
    if simplified:
        title_prefixes.add(simplified)

# Rassemblement de tous les acronymes potentiels
all_text = " ".join(" ".join(str(value) for value in study.values()) for study in data.values())
acronyms_found = extract_acronyms(all_text)

# Nettoyage
filtered_acronyms = []
for acro in acronyms_found:
    acro_upper = acro.upper()
    keep = True
    for prefix in title_prefixes:
        if acro_upper == prefix or acro_upper.startswith(prefix):
            keep = False
            break
    if keep and len(acro) < 7:
        filtered_acronyms.append(acro)

# Filtrage des acronymes "bizarres"
acronyms_bizarre = []
for acro in filtered_acronyms[:]:
    has_digit = any(char.isdigit() for char in acro)
    lower_count = sum(1 for char in acro if char.islower())
    if has_digit or lower_count >= 2:
        acronyms_bizarre.append(acro)
        filtered_acronyms.remove(acro)

# Combine tous les acronymes finaux
final_acronyms = filtered_acronyms + acronyms_bizarre

print(len(final_acronyms))
print("acronymes : ",filtered_acronyms)
print("Acronymes bizarres : ",acronyms_bizarre)

# Sorties
study_to_acronyms = {}
found_acronyms = set()

for study_id, study in data.items():
    text = " ".join(str(v) for v in study.values())
    found = [acro for acro in final_acronyms if acro in text]

    if found:
        study_to_acronyms[study_id] = found
        found_acronyms.update(found)

#Acronymes trouvés par étude
with open(output_json, "w", encoding="utf-8") as f:
    json.dump(study_to_acronyms, f, ensure_ascii=False, indent=2)

not_found_acronyms = sorted(set(found_acronyms))

#Acronymes trouvés (sans étude)
not_found_output = output_json.replace("_section.json", ".json")
with open(not_found_output, "w", encoding="utf-8") as f:
    json.dump(not_found_acronyms, f, ensure_ascii=False, indent=2)


