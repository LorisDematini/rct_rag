"""
We iteratively look for every clinical protocol in the central repository of bdd (URC Saint Louis global repository for RCTs)
for each study, in the folder "PROTOCOLE",
"""

import os
import shutil
import re

# Define source directory and destination directory
source_dir = "V:\\"  # Adjust this if using WSL (e.g., "/mnt/v/")

# Check if source directory exists
if os.path.exists(source_dir):
    # List all entries in the directory and filter only folders
    folders = [entry for entry in os.listdir(source_dir) if os.path.isdir(os.path.join(source_dir, entry))]
    print(f"\nTotal folders in '{source_dir}': {len(folders)}")
else:
    print("\nSource directory not found!")

destination_dir = "C:/DonneesLocales/git_cse/rct_rag/rct_rag/get_bdd/data"
os.makedirs(destination_dir, exist_ok=True) # Ensure destination directory exists

# Define search keyword (case-insensitive)
search_pattern = re.compile(r"(?i)protocol")

# Allowed file types
allowed_extensions = (".doc",".docx")#, ".pdf") #focus on word documents in a first step

# Folders to ignore
ignored_folders = {".Poubelle", "AANNEXE", "AARCHIVES", "Z_URC"}

# Get the list of all folders in source_dir
all_folders = [f for f in os.listdir(source_dir) if os.path.isdir(os.path.join(source_dir, f))]
# Remove ignored folders
filtered_folders = [f for f in all_folders if f not in ignored_folders]
print("Total number of folders (clinical studies)", len(filtered_folders))

# Initialize counters
studies_with_protocol = 0
studies_without_protocol = 0

# Iterate through the remaining directories
for folder in filtered_folders:

    matching_files =[]

    study_path = os.path.join(source_dir, folder)
    protocole_path = os.path.join(study_path, "PROTOCOLE")

    # Check if "PROTOCOLE" folder exists
    if not os.path.exists(protocole_path):
        print(f"❌ No PROTOCOLE folder for study: {folder}")
        studies_without_protocol += 1
        continue  # Skip this study

    print(f"🔍 Searching in PROTOCOLE folder: {protocole_path}")

    # Collect all matching files in the protocole_path and subfolders
    for root, _, files in os.walk(protocole_path):  # protocole_path and subfolders
        for file in files:
            if file.lower().endswith(allowed_extensions) and search_pattern.search(file):
                matching_files.append(os.path.join(root, file))

    if matching_files:
        # Find the latest modified file in the PROTOCOLE folder
        latest_file = max(matching_files, key=os.path.getmtime)
        destination_path = os.path.join(destination_dir, os.path.basename(latest_file))

        # Copy and overwrite existing file
        # shutil.copyfile(latest_file, destination_path)
        with open(latest_file, "rb") as src, open(destination_path, "wb") as dst:
            dst.write(src.read())  # ✅ Reads and writes the entire file correctly to avoid corruption and missing parts

        studies_with_protocol += 1  # Increment count for studies with protocols
        print(f"✅ Copied: {latest_file}")
    else:
        print(f"❌ PROTOCOLE folder exisits but no matching files found in {protocole_path}")
        studies_without_protocol += 1  # Increment count for studies without matching files

# Print final counts
print("\n📊 **Summary:**")
print(f"✅ Studies with at least one protocol file: {studies_with_protocol}")
print(f"❌ Studies without a protocol file: {studies_without_protocol}")

print("\n✅ All matching files copied successfully!")
