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

def categorize_study_sections_full(input_json_path: str, output_json_path: str) -> None:
    """
    Loads a JSON where each study contains section titles and their values.
    For each section title, it matches a predefined category using keyword lists.
    The categorized sections are grouped and saved with normalized study names.
    """
    categories: Dict[str, list] = {
        "TITLE": [
            "name of the study",
            "title",
            "full title", 
        ],
        "JUSTIFICATION": [
            "background",
            "scientific justification", 
            "rationale", 
            "main backgrounds",
        ],
        "OBJECTIVE": [
            "objectives",
            "main objective and primary endpoint",
            "main end-points",
            "primary objective",
            "primary objectives",
            "criteria of assessment",
            "primary objective and assessment criterion",
            "objective and primary endpoint", 
            "objectives and secondary endpoints", 
            "secondary objectives",
            "secondary objectives and endpoints",
            "secondary objectives and assessment criteria",
            "secondary end-points",
            "study endpoints",
            "study objectives",
            "evaluation criteria",
            "questions asked in the caall-f01 protocol",
        ],
        "DESIGN": [
            "study design",
            "design / phase / category",
            "design of the study",
            "design of the trial",
            "experimental design",
            "diagnostic method",
            "reference diagnostic method",
            "scope of the trial",
            "ancillary study",
            "type of study",
        ],
        "INCLUSION CRITERIA": [
            "inclusion criteria",
            "preinclusion criteria",
            "graall-2014/b inclusion criteria",
            "graall-quest inclusion criteria",
            "inclusion criteria observational phase: (n°1,2,3,4,6,7,8,9) interventional phase: (n°1,2,3,4,5,6,7,8).",
            "inclusion criteria   ",
            "inclusion criteria of donors",
            "inclusion criteria of patients",
            "population concerned",
            "population involved",
            "population of study participants",
            "population of trial subjects",
            "indication",
        ],
        "EXCLUSION CRITERIA": [
            "graall-2014/b non inclusion criteria",
            "graall-quest non inclusion criteria",
            "non-preinclusion and non-inclusion criteria",
            "non-inclusion criteria",
            "non inclusion criteria",
            "exclusion criteria observational phase: (n°1,2,3) interventional phase: (n°:1,2,3,4,5,6,7,8).",
            "exclusion criteria",
            "exclusion criteria :",
            "exclusion criteria of patients",
            "exclusion criterion",
        ],
        "INTERVENTION" : [
            "reference treatment",
            "transplant modalities",
            "transplant modalities medical product provided by the sponsor",
            "transplantation modalities",
            "transplants modalities",
            "treatment (transplant modalities)",
            "treatment being tested",
            "treatment",
            "benchmark treatment",
            "comparator strategy and treatment",
            "comparator treatment",
            "concomitant treatments",
            "experimental treatment",
            "experimental drug prescription outside ma",
            "experimental drugs prescription according to ma",
            "experimental group",
            "investigational medicinal product(s)",
            "investigational drug",
            "investigational medicinal product",
            "medicinal product and auxiliairy medicinal products",
            "investigational medicinal products",
            "investigational strategy and medicinal product(s)",
            "investigational medicinal product and auxiliairy medicinal products",
            "study intervention",
            "chemotherapy",
            "challenge agents",
            "comparator",
            "comparator arm",
        ],
        "STATISTICS": [
            "statistical justification of sample size",
            "statistical analysis",
            "statistical power and sample size justification:",
            "first interim analysis",
            "sample size",
        ],
        "DSMB" : [
            "dsmb",
            "dsmb (data safety monitoring board)",
            "dsmb : data safety monitoring board",
            "data safety monitoring board",
            "data safety monitoring board anticipated",
            "independent surveillance committee planned",
            "study will have a data safety monitoring board",
            "trial will have a data monitoring committee",
            "trial will have a data safety monitoring board",
        ],
        "ACRONYM" : [
            "abbreviated title",
            "acronym",
            "acronym/reference",
            "short title",
            "study acronym",
            "clinical trial code",
        ],
        "INVESTIGATOR" : [
            "coordinating investigator",
            "coordinating investigator and scientific director",
            "coordinating investigator and scientific director",
            "coordinating investigators",
            "coordinator",
            "scientific director",
            "scientific director (if applicable)"
        ],
        "NUMBER OF INCLUSIONS": [
            "number of participants included",
            "number of participants chosen",
            "number of selected subjects",
            "number of subjects chosen",
            "number of subjects included",
            "number of subjects required",
        ],
        "SITES" : [
            "number of valued sites",
            "clinical sites",
            "centres: 28",
            "number of sites",
            "number of centers",
            "number of centres",
        ],
        "FUNDING": [
            "study sponsor",
            "sources of funding for the trial",
            "sources of monetary support",
            "sponsor",
            "financing",
            "funding",
            "funding source",
            "funding sources",
            "budget",
        ],
    }
    
    with open(input_json_path, "r", encoding="utf-8") as file_input:
        list_study_content = json.load(file_input)

    grouped_data: Dict[str, Dict[str, list]] = {}

    for study_name, study_content in list_study_content.items():
        normalized_name = clean_study_name(study_name)
        sorted_sections = {category: [] for category in categories}

        for key, value in study_content.items():
            entry_text = f"{key}: {value}"
            norm_key = normalize(key)
            for category, keywords in categories.items():
                if any(normalize(keyword) == norm_key for keyword in keywords):
                    sorted_sections[category].append(entry_text)
                    break

        grouped_data[normalized_name] = sorted_sections

    os.makedirs(os.path.dirname(output_json_path), exist_ok=True)
    with open(output_json_path, "w", encoding="utf-8") as file_output:
        json.dump(grouped_data, file_output, indent=2, ensure_ascii=False)

    print(f"Categorized sections saved to: {output_json_path}")
