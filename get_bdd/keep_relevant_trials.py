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
data_folder = "/mnt/c/DonneesLocales/git_cse/rct_rag/rct_rag/get_bdd/data"
rct_protocols_folder = "/mnt/c/DonneesLocales/git_cse/rct_rag/rct_rag/get_bdd/rct_protocols"
os.makedirs(rct_protocols_folder, exist_ok=True) # Ensure the destination folder exists

# Convert list items to lowercase for case-insensitive comparison
launched_trial_list_lower = [trial.lower() for trial in launched_trial_list]

found_rct = 0

# Iterate through all files in the data folder
for file in os.listdir(data_folder):
    file_path = os.path.join(data_folder, file)
    
    if os.path.isfile(file_path):  # Ensure it's a file (not a directory)
        # Check if the filename contains any launched trial (case insensitive)
        if any(re.search(rf"(?i){trial}", file) for trial in launched_trial_list_lower):
            destination_path = os.path.join(rct_protocols_folder, file)

            # Copy file to rct_protocols, overwriting if needed
            shutil.copy2(file_path, destination_path)
            print(f"✅ Found : {file_path}")
            found_rct+=1


print("\n✅", found_rct, "files copied to rct_protocols!")