import os
import json
from pathlib import Path
from docx import Document
from docx.document import Document as _Document
from docx.oxml.table import CT_Tbl
from docx.oxml.text.paragraph import CT_P
from docx.table import Table
from docx.text.paragraph import Paragraph

def iter_block_items(parent):
    if isinstance(parent, _Document):
        parent_elm = parent.element.body
    else:
        raise ValueError("marche pas")

    for child in parent_elm.iterchildren():
        if isinstance(child, CT_P):
            yield Paragraph(child, parent)
        elif isinstance(child, CT_Tbl):
            yield Table(child, parent)

def is_title_paragraph(paragraph):
    return paragraph.style.name.lower().startswith(('heading', 'title', 'titre'))

def extraire_tableau_summary(entree, sortie):
    Path(sortie).mkdir(parents=True, exist_ok=True)
    
    resultats = {}
    
    for fichier in os.listdir(entree):
        if fichier.endswith('.docx'):
            chemin_complet = os.path.join(entree, fichier)
            try:
                doc = Document(chemin_complet)
                summary_data = None
                summary_pos = -1
                current_pos = 0
                
                for block in iter_block_items(doc):
                    if isinstance(block, Paragraph):
                        if (is_title_paragraph(block) and 
                            ('summary' in block.text.strip().lower() or 
                            '1.2 synopsis' in block.text.strip().lower() or 
                            'study summary' in block.text.strip().lower())):
                            summary_pos = current_pos
                            break
                    current_pos += 1
                
                if summary_pos >= 0:
                    current_pos = 0
                    summary_data = []
                    in_summary_section = False
                    
                    for block in iter_block_items(doc):
                        if current_pos > summary_pos:
                            if isinstance(block, Table):
                                table_data = []
                                for row in block.rows:
                                    row_data = []
                                    for cell in row.cells:
                                        cell_text = cell.text.strip().replace('\t', ' ')
                                        row_data.append(cell_text)
                                    table_data.append(row_data)
                                summary_data.extend(table_data)
                                in_summary_section = True
                            elif isinstance(block, Paragraph):
                                if (is_title_paragraph(block) or 
                                    (block.text.strip() and in_summary_section)):
                                    break
                        current_pos += 1
                
                if summary_data:
                    nom_etude = os.path.splitext(fichier)[0]
                    resultats[nom_etude] = summary_data
                else:
                    print(f"Rien après SUMMARY dans {fichier}")
                
            except Exception as e:
                print(f"Erreur avec {fichier}: {str(e)}")
    
    output_path = os.path.join(sortie, "summary_tables.json")
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(resultats, f, ensure_ascii=False, indent=4)
    
    print(f"\nRésultats : {len(resultats)} fichiers avec tableaux")
    return resultats

# Chemins
entree = "/home/loris/Stage/STAGE/Test/BDD_DOC_TRUE"
sortie = "/home/loris/Stage/STAGE/Test/db_sortie_block/DOC"

# Exécution
resultats = extraire_tableau_summary(entree, sortie)