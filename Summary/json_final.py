import json
import csv
from collections import defaultdict

# Chemins des fichiers
input_path = '/home/loris/Stage/STAGE/Test/db_sortie_block/DOC/Extract/summary_tables_gather.json'
output_json_path = '/home/loris/Stage/STAGE/Test/db_sortie_block/DOC/Summary/FULL.json'
output_csv_path = '/home/loris/Stage/STAGE/Test/db_sortie_block/DOC/Summary/titles_coverage.csv'
summary_json_path = '/home/loris/Stage/STAGE/Test/db_sortie_block/DOC/Summary/summary_tables_gather.json'  # Le fichier JSON des résumés

# Mapping des titres vers les catégories générales (pas besoin de "SUMMARY" ici)
title_groups = {
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

# Charger le fichier JSON des résumés
with open(summary_json_path, 'r', encoding='utf-8') as f:
    summaries_data = json.load(f)

# Préparer les structures de données
grouped_data = {}
coverage_data = []
title_mapping = defaultdict(set)

# Traiter chaque étude
for study_id, sections in studies_data.items():
    grouped_sections = defaultdict(list)
    title_presence = {'Study ID': study_id}

    # Initialiser toutes les catégories comme absentes
    for group in title_groups.keys():
        title_presence[group] = ''

    # Ajouter directement la section SUMMARY depuis le fichier des résumés
    if study_id in summaries_data:
        # Récupérer le texte de la section "SUMMARY" uniquement à partir du fichier summary_tables_gather.json
        summary_text = summaries_data[study_id].get("SUMMARY", "").strip()
        if summary_text:
            grouped_sections["SUMMARY"] = [summary_text]
            title_presence["SUMMARY"] = 'true'

    # Traiter les autres sections
    for section in sections:
        if not isinstance(section, dict):
            continue
            
        # Récupérer le texte (soit 'texte' soit 'paragraphes')
        if 'texte' in section:
            section_text = section['texte'].strip()
        elif 'paragraphes' in section:
            section_text = " ".join([p.strip() for p in section['paragraphes'] if isinstance(p, str)]).strip()
        else:
            continue

        if not section_text:  # Ignorer les sections vides
            continue

        section_title = section['titre'].strip().lower()
        matched_group = next((group for kw, group in keyword_to_group.items() if kw in section_title), None)
        
        if matched_group:
            grouped_sections[matched_group].append(section_text)
            title_presence[matched_group] = 'true'
            title_mapping[section_title].add(section['titre'])

    # Fusionner les textes pour chaque section en un seul texte
    final_grouped = {}
    for group, texts in grouped_sections.items():
        # Fusionner tous les textes de la section en un seul, séparés par des espaces
        merged_text = " ".join(texts)
        final_grouped[group] = merged_text

    grouped_data[study_id] = final_grouped
    coverage_data.append(title_presence)

# Sauvegarder le JSON groupé
with open(output_json_path, 'w', encoding='utf-8') as f:
    json.dump(grouped_data, f, indent=4, ensure_ascii=False)

# Mettre à jour fieldnames pour inclure 'SUMMARY'
fieldnames = ['Study ID', 'SUMMARY'] + list(title_groups.keys())

# Sauvegarder le CSV de couverture
with open(output_csv_path, 'w', encoding='utf-8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(coverage_data)

# Sauvegarder le mapping des titres
title_mapping_path = '/home/loris/Stage/STAGE/Test/db_sortie_block/DOC/Summary/title_mapping_FULL.json'
with open(title_mapping_path, 'w', encoding='utf-8') as f:
    json.dump({k: list(v) for k, v in title_mapping.items()}, f, indent=4, ensure_ascii=False)

print("Traitement terminé avec succès !")
