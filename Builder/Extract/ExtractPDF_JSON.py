import os
import json
import logging
import pdfplumber
from typing import Dict

logging.getLogger("pdfminer").setLevel(logging.ERROR)


def extract_study_tables_from_pdfs(pdf_folder: str, output_json_path: str) -> None:
    """
    This function looks for tables in each PDF that contain English keywords for the beginning of the tab like "title" or "study".
    Once the table is found, it extracts key-value pairs (from 2-column rows) until it either
    finishes reading the file or encounters a French keyword ("titre"), which signals the end
    of the relevant table. The result is stored in a dictionary where each PDF is represented by
    a study acronym (found in the content or derived from the filename), and saved in JSON format.
    """
    keywords_en = ["title", "study"]
    stopword_fr = "titre"
    final_data: Dict[str, Dict[str, str]] = {}

    for file_name in os.listdir(pdf_folder):
        #Check if file is PDF 
        if not file_name.lower().endswith(".pdf"):
            continue

        file_path = os.path.join(pdf_folder, file_name)
        with pdfplumber.open(file_path) as pdf:
            capture_mode = False
            stop_extraction = False
            extracted_rows = []

            for page in pdf.pages:
                if stop_extraction:
                    break

                tables = page.extract_tables()
                if not tables:
                    # If already in capture mode and no tables remain, stop extraction
                    if capture_mode:
                        break
                    continue

                for table in tables:
                    if not table or stop_extraction:
                        continue

                    # Start extraction if any English keyword is found
                    if not capture_mode:
                        found_title = any(
                            any(cell and keyword in cell.lower() for keyword in keywords_en for cell in row)
                            for row in table
                        )
                        if found_title:
                            capture_mode = True
                        else:
                            continue

                    for row in table:
                        if not row:
                            continue

                        # Stop extraction if French keyword is detected
                        if any(cell and stopword_fr in cell.lower() for cell in row):
                            print(f"Stopping extraction for {file_name}: French table detected.")
                            stop_extraction = True
                            break

                        # Handle 2-column rows as key-value pairs
                        if len(row) == 2:
                            titre = row[0].strip() if row[0] else ""
                            valeur = row[1].strip() if row[1] else ""
                            if valeur:
                                extracted_rows.append({"Titre": titre, "Valeur": valeur})

                        # Handle 1-column continuation lines (append to previous value)
                        elif len(row) == 1 and row[0]:
                            valeur = row[0].strip()
                            if valeur and extracted_rows:
                                extracted_rows[-1]["Valeur"] += " " + valeur

        # Build dictionary for the current PDF
        data: Dict[str, str] = {}
        acronyme = None
        for row in extracted_rows:
            titre = row["Titre"]
            valeur = row["Valeur"]
            data[titre] = valeur

            # Try to find an acronym key to use as unique identifier
            if not acronyme and ("ACRONYM" in titre.upper() or "ACRONYME" in titre.upper() or "ABBREVIATED" in titre.upper()):
                acronyme = valeur.strip().split()[0].replace(":", "")

        # Fallback to file name if no acronym was found
        if not acronyme:
            acronyme = os.path.splitext(file_name)[0]

        final_data[acronyme] = data

    # Ensure the output directory exists
    os.makedirs(os.path.dirname(output_json_path), exist_ok=True)

    # Save extracted data to JSON
    with open(output_json_path, "w", encoding="utf-8") as f:
        json.dump(final_data, f, indent=4, ensure_ascii=False)

    print(f"Extraction complete: {len(final_data)} files processed.\nResult saved to {output_json_path}")
