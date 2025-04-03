import json

summary_path = '/home/loris/Stage/STAGE/Test/db_sortie_block/DOC/summary_tables.json'
extract_path = '/home/loris/Stage/STAGE/Test/db_sortie_block/DOC/extract_docx.json'
output_path = '/home/loris/Stage/STAGE/Test/db_sortie_block/DOC/summary_tables_gather.json'

with open(summary_path, 'r', encoding='utf-8') as f:
    summary_data = json.load(f)

with open(extract_path, 'r', encoding='utf-8') as f:
    extract_data = json.load(f)

for study_id in summary_data:
    if study_id in extract_data:
        for section in extract_data[study_id]:
            if isinstance(section, dict) and (section.get('titre') == 'SUMMARY' or section.get('titre') == '1.2 SYNOPSIS' or section.get('titre') == 'STUDY SUMMARY'):
                paragraphs = []
                for key_value_pair in summary_data[study_id]:
                    if len(key_value_pair) >= 2:
                        paragraph = f"{key_value_pair[0]}: {key_value_pair[1]}"
                        paragraphs.append(paragraph)
                
                section['paragraphes'] = paragraphs
                break

with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(extract_data, f, indent=4, ensure_ascii=False)

print("Traitement terminé avec succès!")