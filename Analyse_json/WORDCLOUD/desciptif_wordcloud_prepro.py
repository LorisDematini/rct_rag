import json
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import os

# Configuration
output_dir = "/home/loris/Stage/STAGE/Test/db_sortie_block/DOC/analysis/WORDCLOUD/Resultat_Prepro"
os.makedirs(output_dir, exist_ok=True)

def load_preprocessed_data(filepath):
    """Charge directement le fichier JSON pré-traité"""
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def generate_wordclouds(studies, sections=['SUMMARY','SCIENTIFIC JUSTIFICATION','OBJECTIVES',
                                         'METHODOLOGY','PROCEDURE','ELIGIBILITY',
                                         'DATA MANAGEMENT','STATISTICAL']):
        
    for section in sections:
        plt.figure(figsize=(24, 16))
        
        studies_data = [(name, data[section]) 
                      for name, data in studies.items() 
                      if section in data and data[section].strip()]
        
        if not studies_data:
            print(f"Aucune donnée valide pour la section {section}")
            continue
            
        num_studies = len(studies_data)
        ncols = min(2, num_studies)
        nrows = (num_studies + ncols - 1) // ncols
        
        for i, (study_name, text) in enumerate(studies_data, 1):
            ax = plt.subplot(nrows, ncols, i)
            
            try:
                wordcloud = WordCloud(
                    width=1400,
                    height=800,
                    background_color='white',
                    collocations=False,
                    max_words=150,
                    min_font_size=10,
                    max_font_size=200
                ).generate(text)
                
                ax.imshow(wordcloud, interpolation='bilinear')
                ax.set_title(f'{section} - {study_name}', pad=10, fontsize=12)
                ax.axis('off')
                
            except Exception as e:
                ax.text(0.5, 0.5, f'Erreur: {str(e)}',
                       horizontalalignment='center',
                       verticalalignment='center',
                       fontsize=10,
                       color='red')
                ax.set_title(f'{section} - {study_name}', pad=10, fontsize=12)
                ax.axis('off')
        
        plt.tight_layout()
        plt.savefig(f'{output_dir}/wordcloud_{section.lower()}_processed.png', dpi=300)
        plt.close()

def main():    
    # Chemin vers votre fichier pré-traité
    preprocessed_file = "/home/loris/Stage/STAGE/Test/db_sortie_block/DOC/grouped_titles_preprocessed.json"
    
    studies = load_preprocessed_data(preprocessed_file)
    generate_wordclouds(studies)
    
    print(f"\nNuages de mots générés et sauvegardés dans : {output_dir}")

if __name__ == "__main__":
    main()