import os
import json
import logging
import pdfplumber
logging.getLogger("pdfminer").setLevel(logging.ERROR)

def extract_study_tables_from_pdfs(pdf_folder, output_json_path):
    keywords_en = ["title", "study"]
    stopword_fr= "titre"
    final_data = {}

    for file_name in os.listdir(pdf_folder):
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
                    if capture_mode:
                        break
                    continue

                for table in tables:
                    if not table or stop_extraction:
                        continue

                    # Démarre l'extraction si un mot-clé est détecté
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

                        # Si un mot-clé français est détecté, on arrête
                        if any(cell and stopword_fr in cell.lower() for cell in row):
                            print(f"Arrêt de l'extraction pour {file_name} : tableau FR détecté.")
                            stop_extraction = True
                            break

                        if len(row) == 2:
                            titre = row[0].strip() if row[0] else ""
                            valeur = row[1].strip() if row[1] else ""
                            if valeur:
                                extracted_rows.append({"Titre": titre, "Valeur": valeur})
                        elif len(row) == 1 and row[0]:
                            valeur = row[0].strip()
                            if valeur and extracted_rows:
                                extracted_rows[-1]["Valeur"] += " " + valeur

        # Construction du dictionnaire pour ce PDF
        data = {}
        acronyme = None
        for row in extracted_rows:
            titre = row["Titre"]
            valeur = row["Valeur"]
            data[titre] = valeur
            if not acronyme and ("ACRONYM" in titre.upper() or "ACRONYME" in titre.upper() or "ABBREVIATED" in titre.upper()):
                acronyme = valeur.strip().split()[0].replace(":", "")

        if not acronyme:
            acronyme = os.path.splitext(file_name)[0]

        final_data[acronyme] = data

    os.makedirs(os.path.dirname(output_json_path), exist_ok=True)
    with open(output_json_path, "w", encoding="utf-8") as f:
        json.dump(final_data, f, indent=4, ensure_ascii=False)

    print(f"Extraction terminée : {len(final_data)} fichiers traités.\nRésultat écrit dans {output_json_path}")
