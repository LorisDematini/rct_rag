import json
import csv
import os

base_path = os.getcwd()

input_json = os.path.join(base_path, "Sections", "sections_sorted_clean_complet.json")
output_csv = os.path.join(base_path, "Sections", "etudes_verification.csv")


with open(input_json, 'r', encoding='utf-8') as f:
    data = json.load(f)

all_keys = set()
for etude, contenu in data.items():
    if isinstance(contenu, dict):
        all_keys.update(contenu.keys())

all_keys = sorted(all_keys)

rows = []
for etude, contenu in data.items():
    row = {'nom_etude': etude}
    for key in all_keys:
        value = contenu.get(key, '') if isinstance(contenu, dict) else ''
        has_text = any(isinstance(v, str) and v.strip() for v in value)
        row[key] = 'oui' if has_text else 'NON'
        if row[key] == "NON":
            print("\nEtude : ",etude)
            print("Section vide : ",key)
    rows.append(row)

with open(output_csv, 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['nom_etude'] + all_keys)
    writer.writeheader()
    writer.writerows(rows)