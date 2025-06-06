import json

with open("/home/loris/Stage/STAGE/Test/PDF_RE/final_output.json", "r", encoding="utf-8") as f:
    data = json.load(f)

grouped_data = []
x=0
for study_name, study_content in data.items():
    print(study_name)
    x+=1
    print(x)