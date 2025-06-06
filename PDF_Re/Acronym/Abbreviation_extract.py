import os
import pdfplumber
import re
import json
import logging
logging.getLogger("pdfminer").setLevel(logging.ERROR)

PDF_FOLDER = "/home/loris/Stage/STAGE/Test/PDF_RE/PDF"
OUTPUT_JSON_PATH = "/home/loris/Stage/STAGE/Test/PDF_RE/acronym_extracted2.json"
TARGET_KEYWORDS = ["abbreviation", "glossary"]

acronym_pattern = re.compile(r"^\s*([A-Z][A-Z0-9\-]{1,10})[\s:,-]+(.+)$")

all_acronyms = {}

for filename in os.listdir(PDF_FOLDER):
    if filename.lower().endswith(".pdf"):
        filepath = os.path.join(PDF_FOLDER, filename)
        matches = []

        with pdfplumber.open(filepath) as pdf:
            for page_num, page in enumerate(pdf.pages):
                text = page.extract_text()
                if not text:
                    continue
                lines = text.splitlines()
                for line in lines:
                    if any(keyword in line.lower() for keyword in TARGET_KEYWORDS):
                        matches.append(page_num)

            if matches:
                target_page_num = matches[1] if len(matches) >= 2 else matches[0]
                page = pdf.pages[target_page_num]
                page_text = page.extract_text()

                if not page_text:
                    continue

                acronyms_dict = {}
                for line in page_text.splitlines():
                    match = acronym_pattern.match(line)
                    if match:
                        acronym, definition = match.groups()
                        acronyms_dict[acronym.strip()] = definition.strip()

                if acronyms_dict:
                    print(filename)
                    study_name = os.path.splitext(filename)[0]
                    print(study_name)
                    all_acronyms[study_name] = acronyms_dict

with open(OUTPUT_JSON_PATH, "w", encoding="utf-8") as f:
    json.dump(all_acronyms, f, ensure_ascii=False, indent=2)

#GRAAL PAS COMPLET
#RUBI SUR PLUSIEURS PAGES

