import json

input_path = '/home/loris/Stage/STAGE/Test/db_sortie_block/DOC/Summary/summary_tables.json'
output_path = '/home/loris/Stage/STAGE/Test/db_sortie_block/DOC/Summary/Comparaison/summary-title.json'

#Json Source
with open(input_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

summary_only = {}

for study_name, fields in data.items():
    #Valeur only
    merged_text = "\n".join([value for _, value in fields])
    summary_only[study_name] = {"Summary": merged_text}

#Sauvegarde
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(summary_only, f, ensure_ascii=False, indent=2)
