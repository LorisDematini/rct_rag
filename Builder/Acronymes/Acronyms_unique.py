import json
from collections import defaultdict

def get_unique_acronyms(input_json: str, output_json_path: str) -> None:
    """
    This function loads a JSON file containing a mapping of study IDs to acronyms and their
    definitions. It normalizes the acronyms (to lowercase), aggregates all definitions found,
    and keeps only those acronyms that have exactly one unique definition. The result is
    saved to a new JSON file with acronyms in uppercase and definitions in lowercase.
    """
    # Load the final acronym JSON file
    with open(input_json, 'r', encoding='utf-8') as file_input:
        data = json.load(file_input)

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
    with open(output_json_path, "w", encoding="utf-8") as file_final:
        json.dump(unique_acronyms, file_final, ensure_ascii=False, indent=2)

    print("Done")
