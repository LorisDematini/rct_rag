import re

input_txt = "/home/loris/Stage/STAGE/Test/PDF_RE/Sections/sections_output.txt"
output_txt = "/home/loris/Stage/STAGE/Test/PDF_RE/Sections/sections_sorted2.txt"

# categories = {
#     "TiTLE": ["acronym", "title", "abbreviated", "reference", "name"],
#     "PEOPLE" : ["investigator", "coordinating", "director", "coordinator", "representatives"],
#     "JUSTiFiCATiON": ["justification", "rationale", "background"],
#     "OBJECTiF": ["objective", "endpoint", "points"],
#     "DESiGN": ["design", "practical", "procedure", "scope", "risk", "type", "ancillary"],
#     "CRiTERiA": ["inclusion", "exclusion", "criteria", "subjects", "population"],
#     "ADMiN": ["number", "duration", "sources", "sponsor", "sites", "financing", "funding", "budget", "centres", "category", "code", "period", "schedule"],
#     "TREATMENT" : ["treatment", "medical", "transplant", "experimental", "drug", "medicinal", "intervention", "indication", "participants", "benefits", "control", "comparator"],
#     "STATISTICAL": ["statistical", "analysis", "sample"],
#     "DSMB" : ["board", "monitoring", "dsmb", "data", "surveillance"],
#     "OTHER": [],
# }

# Est-ce qu'on accepte "abbreviated title" ?
#"investigational" pour treatment ?
#leukemia-oriented biological assessments ?
categories = {
    "TITLE": [
        "name of the study",
        "title",
        "full title", 
        "short title", 
        "abbreviated title",
    ],
    "JUSTIFICATION": [
        "background",
        "scientific justification", 
        "rationale", 
        "main backgrounds",
        "background therapy",
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


def normalize(text):
    return re.sub(r'\s+', ' ', text.strip().lower())


with open(input_txt, encoding="utf-8") as f:
    content = f.read()

items = content.split("- ")
items = [item.strip() for item in items if item.strip()]

sorted_sections = {category: [] for category in categories}

for item in items:
    found = False
    full_line = item.replace("\n", " ")
    norm_title = normalize(full_line)
    for category, keywords in categories.items():
        for keyword in keywords:
            if normalize(keyword) == norm_title:
                sorted_sections[category].append(item)
                found = True
                break
        if found:
            break
    if not found:
        sorted_sections["OTHER"].append(item)

with open(output_txt, "w", encoding="utf-8") as f:
    for category, items in sorted_sections.items():
        f.write(f"## {category}\n")
        for item in items:
            f.write(f"- {item}\n")
        f.write("\n")
        