import json
import re

input_json = "/home/loris/Stage/STAGE/Test/PDF_RE/final_output.json"
output_json = "/home/loris/Stage/STAGE/Test/PDF_RE/Sections/sections_sorted.json"

# categories = {
#     "TITLE": ["acronym", "title", "abbreviated", "reference", "name"],
#     "PEOPLE": ["investigator", "coordinating", "director", "coordinator", "representatives"],
#     "JUSTIFICATION": ["justification", "rationale", "background"],
#     "OBJECTIF": ["objective", "endpoint", "points"],
#     "DESIGN": ["design", "practical", "procedure", "scope", "risk", "type", "ancillary"],
#     "CRITERIA": ["inclusion", "exclusion", "criteria", "subjects", "population"],
#     "ADMIN": ["number", "duration", "sources", "sponsor", "sites", "financing", "funding", "budget", "centres", "category", "code", "period", "schedule"],
#     "TREATMENT": ["treatment", "medical", "transplant", "experimental", "drug", "medicinal", "intervention", "indication", "participants", "benefits", "control", "comparator"],
#     "STATISTICAL": ["statistical", "analysis", "sample"],
#     "DSMB": ["board", "monitoring", "dsmb", "data", "surveillance"],
#     "OTHER": [],
# }

categories = {
    "TITLE": [
        "name of the study",
        "title",
        "full title", 
        "short title", 
        "abbreviated title",
        "abbreviation"
    ],
    "JUSTIFICATION": [
        "background",
        "scientific justification", 
        "rationale", 
        "main backgrounds",
        "background therapy",
        "type of study",
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
    ],
    "DESIGN": [
        "study design",
        "design / phase / category",
        "design of the study",
        "design of the trial",
        "experimental design",
        "practical procedure",
        "practical course",
        "practical implementation",
        "other procedures added by the research",
        "other acts added by research",
        "other interventions added by the study",
        "ancillary study",
        "added risks of the research",
        "added risks through research",
        "risks added by the research",
        "risks added by the clinical trial",
        "risks added by the study",
        "risks added by the trial",
        "risks and burdens added by the study",
        "minimal risks and constraints added by the study",
        "risk factors definition",
        "evaluation criteria",
        "sample size",
        "diagnostic method",
        "randomization (interventional phase)",
        "reference diagnostic method",
    
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
    "TREATMENT" : [
        "reference treatment",
        "transplant modalities",
        "transplant modalities medical product provided by the Sponsor",
        "transplantation modalities",
        "transplants modalities",
        "treatment (transplant modalities)",
        "treatment being tested",
        "treatment schedules",
        "treatment",
        "benchmark treatment",
        "comparator strategy and treatment",
        "comparator treatment",
        "concomitant treatments",
        "experimental treatment",
        "experimental drug prescription outside ma",
        "experimental drugs prescription according to ma",
        "experimental group",
        "intervention under investigation",
        "interventions added by the study",
        "interventions added for the study",
        "interventions added for the trial",
        "interventions or product under investigation",
        "investigational medicinal product(s)",
        "investigational drug",
        "investigational medicinal product",
        "medicinal product and auxiliairy medicinal products",
        "investigational medicinal products",
        "investigational strategy and medicinal product(s)",
        "investigational medicinal product and auxiliairy medicinal products",
        "chemotherapy",
        #PAS SUR
        "comparator",
        "comparator arm",
        "control group",
        "definitions"
    ],
    "STATISTICAL": [
        "statistical justification of sample size",
        "statistical analysis",
        "statistical power and sample size justification:",
        "first interim analysis",
    ],
    "OTHER": [],
}

def clean_study_name(name):
    if "_" in name:
        name = name.split("_")[0]
    return name.upper()

def normalize(text):
    return re.sub(r'\s+', ' ', text.strip().lower())

with open(input_json, "r", encoding="utf-8") as f:
    data = json.load(f)

grouped_data = {}

for study_name, study_content in data.items():
    study_name = clean_study_name(study_name)
    sorted_sections = {category: [] for category in categories}

    for key, value in study_content.items():
        entry_text = f"{key}: {value}"
        norm_key = normalize(key)
        found = False
        for category, keywords in categories.items():
            for keyword in keywords:
                if normalize(keyword) == norm_key:
                    sorted_sections[category].append(entry_text)
                    found = True
                    break
            if found:
                break
        if not found:
            sorted_sections["OTHER"].append(entry_text)

    grouped_data[study_name] = sorted_sections

with open(output_json, "w", encoding="utf-8") as f:
    json.dump(grouped_data, f, indent=2, ensure_ascii=False)

print("FIN")
