import json
import re
from collections import defaultdict

input_json = "/home/loris/Stage/STAGE/Test/PDF_RE/final_output.json"
output_counts = "/home/loris/Stage/STAGE/Test/PDF_RE/Sections/match_categories.json"

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

    "RISKS": [
        "Risks added by the research",
        "Risks added by the clinical trial",
        "Risks added by the study",
        "Risks added by the trial",
        "Risks and burdens added by the study",
        "Added risks of the research",
        "Added risks through research",
        "Minimal risks and constraints added by the study",
        "risk factors definition",
    ],

    "TREATMENT BIS":[
        # BIZARRE
        "Leukemia-oriented biological assessments",
        "comparator",
        "comparator arm",
        "control group",
        "background therapy",
    ],
    "PROCEDURE":[
        "practical procedure",
        "practical course",
        "practical implementation",
        "other acts added by research",
        "other procedures added by the research",
        "randomization (interventional phase)",
        "Identification of subjects",
        "intervention under investigation",
        "interventions added by the study",
        "interventions added for the study",
        "interventions added for the trial",
        "interventions or product under investigation",
        "other interventions added by the study",
    ],
    "EXPECTED BENEFITS": [
        "Expected benefits",
        "Expected benefits for the participants and for society",
    ],


    "DSMB" : [
        "DSMB",
        "DSMB (Data Safety Monitoring Board)",
        "DSMB : Data safety monitoring board",
        "Data Safety Monitoring Board",
        "Data Safety Monitoring Board anticipated",
        "Independent surveillance committee planned",
        "Study will have a Data Safety Monitoring Board",
        "Trial will have a Data Monitoring Committee",
        "Trial will have a Data Safety Monitoring Board",
    ],
    "TITRES NON VOULUES" : [
        "Abbreviated title",
        "Acronym",
        "Acronym/reference",
        "Short Title",
        "Study Acronym",
        "Clinical Trial Code",
    ],
    "PEOPLE" : [
        "Coordinating Investigator",
        "Coordinating investigator",
        "Coordinating investigator and Scientific Director",
        "Coordinating investigator and Scientific director",
        "Coordinating investigators",
        "coordinating investigator",
        "Coordinator",
        "Scientific Director",
        "Scientific Director (if applicable)",
        "Study committee representatives",
    ],
    "NUMBERS": [
        "Number of enrolments expected per site and per month",
        "Number of inclusions expected per center and per month",
        "Number of inclusions expected per centre and per month",
        "Number of participants included",
        "Number of inclusions expected /centre and month",
        "Number of inclusions under center per month",
        "Number of participants chosen",
        "Number of selected subjects",
        "Number of subjects chosen",
        "Number of subjects included",
        "Number of subjects required",
    ],
    "SITES" : [
        "Number of valued sites",
        "Clinical Sites",
        "Centres: 28",
        "Number of sites",
        "Number of centers",
        "Number of centres",
    ],
    "MONETARY": [
        "Study Sponsor",
        "Sources of funding for the trial",
        "Sources of monetary support",
        "Sponsor",
        "Financing",
        "Funding",
        "Funding source",
        "Funding sources",
        "Budget",
    ],
    "DURATION" : [
        "Duration of the study",
        "Duration of the trial",
        "Research duration",
        "treatment schedules",
        "Schedule for the study",
        "Study Duration",
        "Research period",
    ],
    "INFORMATIONS": [
        "Category",
        "EU-CT number",
        "EudraCT Number",
        "SAEs",
        "Scope of the study", 
    ],
    "SPECIFIC": [
        #Ne rentre nul part parfaitement
        "ASPARAGINASE- Oriented assays",
        "Add-on studies",
        "MRD monitoring",
        "Device(s) under investigation", 
        "definitions",
    ],
    "OTHER": [],
}

#On normalise en enlevant les majuscules et le signes de tabulation, espaces etc.
def normalize(text):
    return re.sub(r'\s+', ' ', text.strip().lower())

with open(input_json, "r", encoding="utf-8") as f:
    data = json.load(f)

final_counts = {}

for category, keywords in categories.items():
    keyword_counts = {}
    for keyword in keywords:
        norm_keyword = normalize(keyword)
        count = 0
        for study in data.values():
            for key in study.keys():
                #On vérifie que ce soit la même chose après normalisation
                if normalize(key) == norm_keyword:
                    count += 1
        if count > 0:
            keyword_counts[f"{keyword}"] = count
    
    if keyword_counts:
        #Total de sous titre trouvés
        total = sum(keyword_counts.values())
        final_counts[f"{category} [{total}]"] = keyword_counts

with open(output_counts, "w", encoding="utf-8") as f_out:
    json.dump(final_counts, f_out, indent=2, ensure_ascii=False)
