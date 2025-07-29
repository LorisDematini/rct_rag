import os
import json

def merge_acronym_jsons(json1_path: str, json2_path: str, output_path: str) -> None:
    """
    This function loads two JSON files where each key is a study ID and each value
    is a dictionary of acronym-definition pairs. It merges the acronym dictionaries
    per study. The final merged result is saved as a final acronym JSON file.
    """
    # Load
    with open(json1_path, 'r', encoding='utf-8') as f1, open(json2_path, 'r', encoding='utf-8') as f2:
        data1 = json.load(f1)
        data2 = json.load(f2)

    fusion = {}  #Merged result 

    # Union of study's ID
    all_keys = set(data1.keys()) | set(data2.keys())

    for key in all_keys:
        # Get the acronym dictionaries for each study ID
        acronyms1 = data1.get(key, {})
        acronyms2 = data2.get(key, {})

        # Merge the two dictionaries
        merged_acronyms = {**acronyms2, **acronyms1}

        # Store thr acronyms under the study ID
        fusion[key] = merged_acronyms

    # Save
    with open(output_path, 'w', encoding='utf-8') as fout:
        json.dump(fusion, fout, ensure_ascii=False, indent=2)

    print(f"Merged {len(data1)} + {len(data2)} studies => {len(fusion)} entries written to {output_path}")
