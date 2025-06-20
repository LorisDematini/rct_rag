import json
import os

base_path = os.getcwd()

json1_path = os.path.join(base_path, "Acronym", "acronyms_etude.json")
json2_path = os.path.join(base_path, "Acronym", "acronym_extracted_pdf.json")
output_path = os.path.join(base_path, "Acronym", "extracted_acronym_final.json")

with open(json1_path, 'r', encoding='utf-8') as f1, open(json2_path, 'r', encoding='utf-8') as f2:
    data1 = json.load(f1)
    data2 = json.load(f2)

    fusion = {**data1, **data2}

with open(output_path, 'w', encoding='utf-8') as fout:
    json.dump(fusion, fout, ensure_ascii=False, indent=2)