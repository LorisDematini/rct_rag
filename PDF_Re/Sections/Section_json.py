import json

json_file = "/home/loris/Stage/STAGE/Test/PDF_RE/final_output.json"
output_txt = "/home/loris/Stage/STAGE/Test/PDF_RE/Sections/sections_output.txt"

with open(json_file, encoding="utf-8") as f:
    data = json.load(f)

sections = set()

for study_id, study_data in data.items():
    for key in study_data.keys():
        sections.add(key)

with open(output_txt, "w", encoding="utf-8") as f:
    for section in sorted(sections):
        f.write(f"- {section}\n")