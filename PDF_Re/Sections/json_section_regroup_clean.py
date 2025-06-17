import json
import re

input_json = "/home/loris/Stage/STAGE/Test/PDF_RE/final_output.json"
output_json = "/home/loris/Stage/STAGE/Test/PDF_RE/Sections/sections_sorted_clean.json"

categories = {
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
        #Bizarre
        "Questions asked in the CAALL-F01 protocol",
    ],
    "DESIGN": [
        "Study Design",
        "design / phase / category",
        "design of the study",
        "design of the trial",
        "experimental design",
        "diagnostic method",
        "reference diagnostic method",
        "Scope of the trial",
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
        "Indication",
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
        "Study Intervention",
        "Study intervention",
        "chemotherapy",
        "Challenge agents",
    ],
    "STATISTICAL": [
        "statistical justification of sample size",
        "statistical analysis",
        "statistical power and sample size justification:",
        "first interim analysis",
        "sample size",
    ],

    # "RISKS": [
    #     "Risks added by the research",
    #     "Risks added by the clinical trial",
    #     "Risks added by the study",
    #     "Risks added by the trial",
    #     "Risks and burdens added by the study",
    #     "Added risks of the research",
    #     "Added risks through research",
    #     "Minimal risks and constraints added by the study",
    #     "risk factors definition",
    # ],

    # "TREATMENT BIS":[
    #     # BIZARRE
    #     "Leukemia-oriented biological assessments",
    #     "comparator",
    #     "comparator arm",
    #     "control group",
    #     "background therapy",
    # ],
    # "PROCEDURE":[
    #     "practical procedure",
    #     "practical course",
    #     "practical implementation",
    #     "other acts added by research",
    #     "other procedures added by the research",
    #     "randomization (interventional phase)",
    #     "Identification of subjects",
    #     "intervention under investigation",
    #     "interventions added by the study",
    #     "interventions added for the study",
    #     "interventions added for the trial",
    #     "interventions or product under investigation",
    #     "other interventions added by the study",
    # ],
    # "EXPECTED BENEFITS": [
    #     "Expected benefits",
    #     "Expected benefits for the participants and for society",
    # ],
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
        # if not found:
            # sorted_sections["OTHER"].append(entry_text)

    grouped_data[study_name] = sorted_sections

with open(output_json, "w", encoding="utf-8") as f:
    json.dump(grouped_data, f, indent=2, ensure_ascii=False)

print("FIN")
