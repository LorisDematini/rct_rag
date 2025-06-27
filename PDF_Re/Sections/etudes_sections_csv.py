import json
import csv
import os

base_path = os.getcwd()

input_json = os.path.join(base_path, "Sections", "sections_sorted_clean_complet.json")
output_csv = os.path.join(base_path, "Sections", "etudes_verification.csv")
output_txt = os.path.join(base_path, "Sections", "etudes_verification.txt")

with open(input_json, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Conserve l’ordre d’apparition des clés dans le premier dictionnaire rencontré
all_keys = []
seen_keys = set()
for contenu in data.values():
    if isinstance(contenu, dict):
        for key in contenu.keys():
            if key not in seen_keys:
                seen_keys.add(key)
                all_keys.append(key)

rows = []
etudes_incompletes = {}
total_sections_manquantes = 0
sections_absences_counter = {key: 0 for key in all_keys}

for etude, contenu in data.items():
    row = {'nom_etude': etude}
    missing_sections = []

    for key in all_keys:
        value = contenu.get(key, '') if isinstance(contenu, dict) else ''
        has_text = any(isinstance(v, str) and v.strip() for v in value)
        row[key] = 'oui' if has_text else 'NON'
        
        if row[key] == 'NON':
            missing_sections.append(key)
            total_sections_manquantes += 1
            sections_absences_counter[key] += 1

    if missing_sections:
        etudes_incompletes[etude] = missing_sections

    rows.append(row)

# Sauvegarde CSV
with open(output_csv, 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['nom_etude'] + all_keys)
    writer.writeheader()
    writer.writerows(rows)

# Sauvegarde TXT
with open(output_txt, 'w', encoding='utf-8') as f:
    f.write(f"Nombre d'études avec au moins une section manquante : {len(etudes_incompletes)}\n")
    f.write(f"Nombre total de sections manquantes (toutes études confondues) : {total_sections_manquantes}\n\n")

    for etude, missing in etudes_incompletes.items():
        f.write(f"Étude : {etude}\n")
        f.write(f"Sections manquantes : {', '.join(missing)}\n\n")
    
    f.write("Fréquence des sections manquantes :\n")
    for section, count in sections_absences_counter.items():
        if count > 0:
            f.write(f"- {section} : {count}\n")
