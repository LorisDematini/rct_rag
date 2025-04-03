import os
import json
from pathlib import Path
from docx import Document

def extraire_titres_avec_paragraphes(entree, sortie):
    Path(sortie).mkdir(parents=True, exist_ok=True)
    
    resultats = {}
    
    for fichier in os.listdir(entree):
        if fichier.endswith('.docx'):
            chemin_complet = os.path.join(entree, fichier)
            try:
                doc = Document(chemin_complet)
                sections = []
                current_section = None
                stop_processing = False
                
                for para in doc.paragraphs:
                    if stop_processing:
                        break
                        
                    if para.style.name.startswith('Heading'):
                        lower_text = para.text.lower()
                        
                        if ('bibliographie' in lower_text or 
                            'bibliography' in lower_text or
                            'form' in lower_text or
                            'française' in lower_text or
                            'mention' in lower_text or
                            'questionnaire' in lower_text or
                            'publication' in lower_text or
                            'insurance' in lower_text or
                            'funding' in lower_text or
                            'archiving' in lower_text or
                            (not para.text.strip() and not para.text.isupper())):
                            continue
                            
                        if any(word in lower_text for word in ['annexe', 'annexes', 'appendix']):
                            stop_processing = True
                            break
                            
                        if current_section:
                            if current_section['paragraphes'] or current_section['titre'].isupper():
                                sections.append(current_section)
                        
                        current_section = {
                            'titre': para.text.strip().replace('\t', ' '),
                            'paragraphes': []
                        }
                    else:
                        if current_section and para.text.strip():
                            cleaned_text = para.text.strip().replace('\t', ' ')
                            current_section['paragraphes'].append(cleaned_text)
                
                if current_section and not stop_processing and (current_section['paragraphes'] or current_section['titre'].isupper()):
                    sections.append(current_section)
                
                if sections:
                    nom_etude = os.path.splitext(fichier)[0]
                    resultats[nom_etude] = sections
                
            except Exception as e:
                print(f"Erreur avec {fichier}: {e}")
    
    output_path = os.path.join(sortie, "extract_docx.json")
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(resultats, f, ensure_ascii=False, indent=4)
    
    return resultats

entree = "/home/loris/Stage/STAGE/Test/BDD_DOC_TRUE"
sortie = "/home/loris/Stage/STAGE/Test/db_sortie_block/DOC"

resultats = extraire_titres_avec_paragraphes(entree, sortie)
print(f"{len(resultats)} fichiers traités.")