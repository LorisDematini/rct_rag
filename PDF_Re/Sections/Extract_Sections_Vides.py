import json

input_json_path = '/home/loris/Stage/STAGE/Test/PDF_RE/Sections/sections_sorted_clean.json'
output_json_path = '/home/loris/Stage/STAGE/Test/PDF_RE/Sections/sections_vides.json'

with open(input_json_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

sections_vides = {}

for study_name, study_content in data.items():
    empty_sections = []
    for key, value in study_content.items():
        if not key.strip() or not value or all(not str(v).strip() for v in value):
            empty_sections.append(key)
    if empty_sections:
        sections_vides[study_name] = empty_sections

with open(output_json_path, 'w', encoding='utf-8') as f:
    json.dump(sections_vides, f, ensure_ascii=False, indent=2)
