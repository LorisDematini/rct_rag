import pdfplumber
import re
import json
import logging
import os
logging.getLogger("pdfminer").setLevel(logging.ERROR)

PDF_PATH = "/home/loris/Stage/STAGE/Test/PDF_RE/PDF/RUBI_protocole_v8-0_20210519_signe.pdf"
TARGET_PAGE_NUM = 15
OUTPUT_JSON_PATH = "/home/loris/Stage/STAGE/Test/PDF_RE/acronym_extract_pageOnly.json"

acronym_pattern = re.compile(r"^\s*([A-Z][A-Z0-9\-]{1,10})[\s:,-]+(.+)$")

all_acronyms = {}

with pdfplumber.open(PDF_PATH) as pdf:
    if TARGET_PAGE_NUM >= len(pdf.pages):
        raise ValueError(f"Le fichier PDF n'a que {len(pdf.pages)} pages. Page demandée : {TARGET_PAGE_NUM}")

    page = pdf.pages[TARGET_PAGE_NUM]
    page_text = page.extract_text()

    if not page_text:
        print(f"Aucun texte trouvé à la page {TARGET_PAGE_NUM}")
    else:
        acronyms_dict = {}
        for line in page_text.splitlines():
            match = acronym_pattern.match(line)
            if match:
                acronym, definition = match.groups()
                acronyms_dict[acronym.strip()] = definition.strip()

        if acronyms_dict:
            study_name = os.path.splitext(os.path.basename(PDF_PATH))[0]
            all_acronyms[study_name] = acronyms_dict
        else:
            print("Aucun acronyme détecté sur cette page.")

with open(OUTPUT_JSON_PATH, "w", encoding="utf-8") as f:
    json.dump(all_acronyms, f, ensure_ascii=False, indent=2)

print(f"Acronymes extraits : {all_acronyms}")
