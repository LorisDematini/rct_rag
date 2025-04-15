import json

json_file_path = "/home/loris/Stage/STAGE/Test/db_sortie_block/DOC/Summary/summary_tables.json"
output_file_path = "/home/loris/Stage/STAGE/Test/db_sortie_block/DOC/Summary/summary_tables_gather.json"

def load_data(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:    
        data = json.load(file)
    return data

# Fonction pour transformer le JSON en une section SUMMARY par étude
def create_summary(data):
    summaries = {}
    for study, details in data.items():
        summary = ""
        for item in details:
            summary += f"{item[0]}: {item[1]}\n"
        summaries[study] = {"SUMMARY": summary.strip()}
    return summaries

# Applique la fonction
data = load_data(json_file_path)
summaries = create_summary(data)

# Sauvegarde le résultat dans un nouveau fichier JSON
with open(output_file_path, 'w', encoding='utf-8') as output_file:
    json.dump(summaries, output_file, ensure_ascii=False, indent=4)

print(f"Résultats enregistrés dans {output_file_path}")
