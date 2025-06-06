import json
import os
import pandas as pd
import glob

input_folder = "/home/loris/Stage/STAGE/Test/PDF_RE/BDD/csv"
output_file = "/home/loris/Stage/STAGE/Test/PDF_RE/Etude_CSV/etudes_liste.csv"
abbrev_file = "/home/loris/Stage/STAGE/Test/PDF_RE/Acronym/acronym_extracted.json"
#liste_complet = "/home/loris/Stage/STAGE/Test/PDF_RE/rct_db.csv"

def normalize_etude(etude):
    etude = etude.split("_")[0] 
    etude = etude.split(":")[0]    
    etude = etude.split(" ")[0]
    etude = etude.split("/")[0]
    return etude

results = []
# normalized_existing = set()

for file_path in glob.glob(os.path.join(input_folder, "*.csv")):
    df = pd.read_csv(file_path)
    file_name = os.path.basename(file_path)

    df.columns = [col.strip() for col in df.columns]
    
    abbrev = "Non"
    etude = normalize_etude(file_name)

    if len(df) < 2:
        statut = "vide"
    
    else:
        acronym_row = df[df["Titre"].str.lower().str.contains("acronym", na=False)]
        if not acronym_row.empty:
            etude = acronym_row["Valeur"].values[0]
            etude = normalize_etude(etude)

        statut = "complet"

        with open(abbrev_file, "r", encoding="utf-8") as json_abbrev:
            data = json.load(json_abbrev)
            for key in data.keys():
                if etude.lower() in key.lower():
                    abbrev = "Oui"

    results.append({"Etude": etude, "Statut": statut, "Acronymes": abbrev})
    # normalized_existing.add(normalize(etude))

# df_liste = pd.read_csv(liste_complet, sep=";")
# for etude_nom in df_liste["Etude"].dropna():
#     if normalize(etude_nom) not in normalized_existing:
#         results.append({
#             "Etude": etude_nom,
#             "Statut": "Absent",
#             "Abbreviations": "Non"
#         })

pd.DataFrame(results).to_csv(output_file, index=True)
