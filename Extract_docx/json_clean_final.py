import json
import csv
from collections import defaultdict

# Chemins des fichiers
input_path = '/home/loris/Stage/STAGE/Test/db_sortie_block/DOC/summary_tables_gather.json'
output_json_path = '/home/loris/Stage/STAGE/Test/db_sortie_block/DOC/grouped_titles2.json'
output_csv_path = '/home/loris/Stage/STAGE/Test/db_sortie_block/DOC/titles_coverage.csv'

# Mapping des titres vers les catégories générales
title_groups = {
    "SUMMARY": ["summary", "synopsis", "study summary"],
    "SCIENTIFIC JUSTIFICATION": ["scientific justification", "hypothesis"],
    "OBJECTIVES": ["primary objective", "secondary objectives", "objective"],
    "METHODOLOGY": ["primary endpoint", "secondary endpoints"],
    "PROCEDURE": [
        "design of", "number of participating sites", "participant identification",
        "schedule", "procedure", "baseline visit"
    ],
    "ELIGIBILITY": ["eligibility criteria", "inclusion criteria", "non inclusion criteria", "exclusion criteria"],
    "DATA MANAGEMENT": ["data management", "data entry", "data confidentiality"],
    "STATISTICAL": ["statistical aspects", "statistical methods", "statistical"]
}

# Inverser le mapping pour la recherche
keyword_to_group = {kw: grp for grp, kws in title_groups.items() for kw in kws}

# Charger les données originales
with open(input_path, 'r', encoding='utf-8') as f:
    studies_data = json.load(f)

# Préparer les structures de données
grouped_data = {}
coverage_data = []
title_mapping = defaultdict(set)  # Pour suivre les correspondances trouvées

# Traiter chaque étude
for study_id, sections in studies_data.items():
    grouped_sections = defaultdict(list)  # Stockage temporaire en liste
    title_presence = {'Study ID': study_id}

    for group in title_groups.keys():
        title_presence[group] = ''

    for section in sections:
        if not isinstance(section, dict):
            continue
            
        if 'texte' in section:
            section_text = section['texte'].strip()
        elif 'paragraphes' in section:
            section_text = " ".join(section['paragraphes']).strip()
        else:
            continue

        section_title = section['titre'].strip().lower()
        matched_group = next((group for kw, group in keyword_to_group.items() if kw in section_title), None)
        
        if matched_group:
            grouped_sections[matched_group].append(section_text)
            title_presence[matched_group] = 'true'
            title_mapping[section_title].add(section['titre'])

    # Fusion finale avec déduplication
    grouped_data[study_id] = {
        group: " ".join(list(set(texts))) 
        for group, texts in grouped_sections.items()
    }
    coverage_data.append(title_presence)

    # Convertir defaultdict en dict normal
    grouped_data[study_id] = dict(grouped_sections)
    coverage_data.append(title_presence)

# Sauvegarder le JSON groupé
with open(output_json_path, 'w', encoding='utf-8') as f:
    json.dump(grouped_data, f, indent=4, ensure_ascii=False)

# Sauvegarder le CSV de couverture
fieldnames = ['Study ID'] + list(title_groups.keys())
with open(output_csv_path, 'w', encoding='utf-8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(coverage_data)

# Sauvegarder le mapping des titres
title_mapping_path = '/home/loris/Stage/STAGE/Test/db_sortie_block/DOC/title_mapping.json'
with open(title_mapping_path, 'w', encoding='utf-8') as f:
    json.dump({k: list(v) for k, v in title_mapping.items()}, f, indent=4, ensure_ascii=False)

print("Traitement terminé avec succès !")
