import json
from collections import defaultdict

def get_consistent_unique_acronyms(data):
    # Étape 1 : groupe toutes les définitions pour chaque acronyme (indépendamment de la casse)
    normalized_acronyms = defaultdict(set)
    original_forms = defaultdict(set)

    for study_id, acronyms_dict in data.items():
        for acronym, definition in acronyms_dict.items():
            if acronym and definition:
                normalized = acronym.lower()
                normalized_acronyms[normalized].add(definition.strip().lower())
                original_forms[normalized].add(acronym)

    # Étape 2 : garde ceux qui ont une seule définition
    unique_acronyms = {}
    for norm_acronym, defs in normalized_acronyms.items():
        if len(defs) == 1:
            canonical = norm_acronym.upper()
            unique_acronyms[canonical] = list(defs)[0]

    return unique_acronyms

if __name__ == "__main__":
    input_json = "/home/loris/Stage/STAGE/Test/PDF_RE/TFIDF_SearchEngine_V2/data/extracted_acronym_final.json"
    output_json = "/home/loris/Stage/STAGE/Test/PDF_RE/TFIDF_SearchEngine_V2/data/unique_acronym.json"
    
    with open(input_json, 'r', encoding='utf-8') as f:
        data = json.load(f)

    unique_acronyms = get_consistent_unique_acronyms(data)

    with open(output_json, 'w', encoding='utf-8') as f:
        json.dump(unique_acronyms, f, ensure_ascii=False, indent=2)
