import os
import pdfplumber
import re
import json
import logging
logging.getLogger("pdfminer").setLevel(logging.ERROR)


def extract_acronyms_from_pdfs(pdf_folder, output_json_path):
    # Regular expression to match lines like: "ABC - Some definition"
    acronym_regex = r"^\s*([A-Z][A-Z0-9\-]{1,10})[\s:,-]+(.+)$"

    # Keywords used to identify pages that likely contain acronyms
    target_keywords = ["abbreviation", "glossary"]

    acronym_pattern = re.compile(acronym_regex)

    # Dictionary of acronyms
    all_acronyms = {}

    # Loop over all files in the specified folder
    for filename in os.listdir(pdf_folder):
        # Security PDF
        if not filename.lower().endswith(".pdf"):
            continue

        filepath = os.path.join(pdf_folder, filename)
        matches = []  # To store page numbers containing target keywords

        try:
            # Open the PDF file
            with pdfplumber.open(filepath) as pdf:
                for page_num, page in enumerate(pdf.pages):
                    text = page.extract_text()
                    if not text:
                        continue
                    lines = text.splitlines()
                    
                    # Check if the page contains any target keywords
                    if any(any(keyword in line.lower() for keyword in target_keywords) for line in lines):
                        matches.append(page_num)

                # Skip this file if no page match the keywords
                if not matches:
                    continue

                #First page or second if available
                target_page_num = matches[1] if len(matches) >= 2 else matches[0]
                page = pdf.pages[target_page_num]
                page_text = page.extract_text()
                if not page_text:
                    continue

                acronyms_dict = {}

                # Extract acronym-definition pairs from lines matching the regex
                for line in page_text.splitlines():
                    match = acronym_pattern.match(line)
                    if match:
                        acronym, definition = match.groups()
                        acronyms_dict[acronym.strip()] = definition.strip()

                # Save extracted acronyms if any were found
                if acronyms_dict:
                    raw_name = os.path.splitext(filename)[0]

                    # If the filename starts with a digit, use the part after the dash
                    if re.match(r'^\d', raw_name):
                        parts = raw_name.split('-', 1)
                        study_name = parts[1] if len(parts) > 1 else raw_name
                    else:
                        study_name = raw_name

                    all_acronyms[study_name] = acronyms_dict

        except Exception as e:
            # Print if PDF try fails
            print(f"Error while processing {filename} : {e}")

    # Study ID before _ or /
    cleaned_ids = {
        re.split(r'[_/]', study_id)[0]: acronyms
        for study_id, acronyms in all_acronyms.items()
    }

    # Save
    with open(output_json_path, "w", encoding="utf-8") as f:
        json.dump(cleaned_ids, f, ensure_ascii=False, indent=2)

    print(f"Extraction complete. Result saved to {output_json_path}")
