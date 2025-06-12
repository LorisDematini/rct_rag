import json

json1_path = "/home/loris/Stage/STAGE/Test/PDF_RE/Acronym/final_acronyms.json"
json2_path = "/home/loris/Stage/STAGE/Test/PDF_RE/Acronym/acronyms_with_definitions.json"
output_path = "/home/loris/Stage/STAGE/Test/PDF_RE/Acronym/final_acronyms_parenthese.json"

with open(json1_path, 'r', encoding='utf-8') as f1, open(json2_path, 'r', encoding='utf-8') as f2:
    data1 = json.load(f1)
    data2 = json.load(f2)

    fusion = {**data1, **data2}

with open(output_path, 'w', encoding='utf-8') as fout:
    json.dump(fusion, fout, ensure_ascii=False, indent=2)