import pandas as pd 
import os
import shutil
import re

#Récupération de la liste des études pertinentes
main_csv = pd.read_csv("Liste_etudes - URC.csv")

etat_avancement_list = ["Inclusions en cours",
                        "Inclusions terminées",
                        "Suivi terminé",
                        "Inclusions suspendues",
                        "Etude cloturée"                   
    ]

typologie_list = ["EC",
                  "RIPH1"
    ]

launched_trial_list = main_csv[(main_csv["Etat avancement global"].isin(etat_avancement_list)) & (main_csv["TYPOLOGIE"].isin(typologie_list))]["ETUDE"].tolist()
###################################


# Define source and destination directories
data_folder = "/mnt/c/Users/ohas2/Documents/APHP_save/rag_project/full_db_protocols"
rct_protocols_folder = "/root/work/rct_rag/get_bdd/data"
os.makedirs(rct_protocols_folder, exist_ok=True) # Ensure the destination folder exists

# Convert list items to lowercase for case-insensitive comparison
launched_trial_list_lower = [trial.lower() for trial in launched_trial_list]

found_rct = 0

# Iterate over each trial first
for trial in launched_trial_list_lower:
    print(trial)
    matching_files = []

    # Iterate through all files in the data folder
    for file in os.listdir(data_folder):
        file_path = os.path.join(data_folder, file)

        if (os.path.isfile(file_path) and 
            file.lower().endswith(".pdf") and
            re.search(rf"(?i){trial}", file) and 
            not file.startswith("._") and 
            "pag" not in file.lower() and 
            "impression" not in file.lower()):

            matching_files.append(file_path)

    # If there are matching files, copy the most recently modified one
    if matching_files:
        latest_file = max(matching_files, key=os.path.getmtime)
        destination_path = os.path.join(rct_protocols_folder, os.path.basename(latest_file))

        # Copy the latest file, overwriting if needed
        shutil.copy2(latest_file, destination_path)
        print(f"✅ Copied latest file for trial '{trial}': {latest_file} ➡️ {destination_path}")
        found_rct += 1
    else : 
        print(f"❌ No PROTOCOLE found for trial : {trial}")


print("\n✅", found_rct, "files copied to rct_protocols!")