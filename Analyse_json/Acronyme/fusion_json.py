import os
import json

def merge_and_process_json(input_dir, output_file):
    all_abbreviations = {}

    # Parcours tous les fichiers JSON dans le répertoire donné
    for file_name in os.listdir(input_dir):
        if file_name.endswith(".json"):
            file_path = os.path.join(input_dir, file_name)

            try:
                # Ouvre et charge le contenu de chaque fichier JSON
                with open(file_path, 'r', encoding='utf-8') as json_file:
                    data = json.load(json_file)
                    
                    # Fusionner les données dans le dictionnaire
                    for entry in data:
                        for abbreviation, definition in entry.items():
                            # Si la définition est une liste, la traiter comme un seul élément
                            if isinstance(definition, list):
                                # On prend uniquement la première valeur de la liste
                                definition = definition[0]
                            
                            # Si l'acronyme n'est pas encore dans le dictionnaire, l'ajouter
                            if abbreviation not in all_abbreviations:
                                all_abbreviations[abbreviation] = definition

            except Exception as e:
                print(f"❌ Erreur lors de la lecture du fichier {file_name}: {e}")

    # Sauvegarder le JSON fusionné et traité dans le fichier de sortie
    try:
        with open(output_file, 'w', encoding='utf-8') as output_json_file:
            json.dump(all_abbreviations, output_json_file, ensure_ascii=False, indent=2)
        print(f"✅ JSON fusionné et traité sauvegardé dans {output_file}")
    except Exception as e:
        print(f"❌ Erreur lors de la sauvegarde du fichier fusionné : {e}")

if __name__ == "__main__":
    # Répertoire contenant les fichiers JSON à fusionner
    input_directory = "/home/loris/Stage/STAGE/Test/db_sortie_block/DOC/analysis/Acronyme/"
    # Fichier de sortie pour le JSON fusionné
    output_file = "/home/loris/Stage/STAGE/Test/db_sortie_block/DOC/analysis/Acronyme/final_acronyms_processed.json"
    
    merge_and_process_json(input_directory, output_file)
