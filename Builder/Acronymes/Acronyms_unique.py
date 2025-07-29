import json
from collections import defaultdict

def get_unique_acronyms(input_json, output_json_path):
    # Load the final JSON file
    with open(input_json, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Dictionary of acronyms with set of their definitions
    normalized_acronyms = defaultdict(set)

    # Iterate over each study and every acronyms
    for study_id, acronyms_dict in data.items():
        for acronym, definition in acronyms_dict.items():
            if acronym and definition:
                # Lowercase
                normalized = acronym.lower()

                # Store definitions for every acronym
                normalized_acronyms[normalized].add(definition.strip().lower())

    # Acronyms with a single consistent definition
    unique_acronyms = {}

    for norm_acronym, defs in normalized_acronyms.items():
    # All definitions are exactly the same string
        if len(defs) >= 1 and len(set(defs)) == 1:
            canonical = norm_acronym.upper()  # Key in uppercase 
            unique_acronyms[canonical] = list(defs)[0]  # Get the (unique) definition


    # Save
    with open(output_json_path, "w", encoding="utf-8") as f:
        json.dump(unique_acronyms, f, ensure_ascii=False, indent=2)

    print("Done")
