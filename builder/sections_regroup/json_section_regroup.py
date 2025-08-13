import json
import re
import os
from typing import Dict

def clean_study_name(name: str) -> str:
    """
    Return the study name prefix (before '_' or '/'), in uppercase.
    """
    base = re.split(r'[_/]', name)[0]
    return base.upper()

def normalize(text: str) -> str:
    """
    Normalize text by removing extra spaces and converting to lowercase.
    """
    return re.sub(r'\s+', ' ', text.strip().lower())

def categorize_study_sections(input_json_path: str, output_json_path: str, categories: str)-> None:
    """
    Categorizes study sections based on predefined section titles and groups them accordingly.
    """
    
    # Load input data
    with open(input_json_path, "r", encoding="utf-8") as file_input:
        list_study_content = json.load(file_input)

    grouped_data : Dict[str, Dict[str, list]]= {}

    # Process each study individually
    for study_name, study_content in list_study_content.items():
        normalized_name = clean_study_name(study_name)
        sorted_sections = {category: [] for category in categories}

        for key, value in study_content.items():
            entry_text = f"{key}: {value}"
            norm_key = normalize(key)
            for category, keywords in categories.items():
                if any(normalize(keyword) == norm_key for keyword in keywords):
                    sorted_sections[category].append(entry_text)
                    # Stop at first match
                    break

        grouped_data[normalized_name] = sorted_sections

    # Ckeck if output directory exists
    os.makedirs(os.path.dirname(output_json_path), exist_ok=True)

    # Save the result to output JSON
    with open(output_json_path, "w", encoding="utf-8") as f:
        json.dump(grouped_data, f, indent=2, ensure_ascii=False)

    print(f"Categorized sections saved to: {output_json_path}")