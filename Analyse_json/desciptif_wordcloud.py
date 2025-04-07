import json
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import os
import re
import unicodedata
import nltk
from nltk.corpus import stopwords

# Téléchargements NLTK
nltk.download('stopwords')

# Configuration
output_dir = "/home/loris/Stage/STAGE/Test/db_sortie_block/DOC/analysis/WORDCLOUD"
os.makedirs(output_dir, exist_ok=True)

class TextPreprocessor:
    def __init__(self):
        self.stop_words = set(stopwords.words('english'))
            
    def normalize_text(self, text):
        if not isinstance(text, str):
            return ""
        
        text = text.lower()
        text = unicodedata.normalize('NFKD', text).encode('ASCII', 'ignore').decode('utf-8')
        text = re.sub(r'[^\w\s]', ' ', text)
        text = re.sub(r'\s+', ' ', text).strip()
        
        # Filtrage des stopwords
        words = [word for word in text.split() if word not in self.stop_words]
        return ' '.join(words)

def load_data(filepath):
    """Charge directement le JSON pré-traité"""
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def generate_wordclouds(studies, sections=['SUMMARY','SCIENTIFIC JUSTIFICATION','OBJECTIVES',
                                         'METHODOLOGY','PROCEDURE','ELIGIBILITY',
                                         'DATA MANAGEMENT','STATISTICAL']):
    preprocessor = TextPreprocessor()
    
    for section in sections:
        plt.figure(figsize=(24, 16))
        
        studies_data = [(name, data[section]) 
                      for name, data in studies.items() 
                      if section in data and isinstance(data[section], str) and data[section].strip()]
        
        if not studies_data:
            print(f"Aucune donnée valide pour la section {section}")
            continue
            
        num_studies = len(studies_data)
        ncols = min(2, num_studies)
        nrows = (num_studies + ncols - 1) // ncols
        
        for i, (study_name, text) in enumerate(studies_data, 1):
            ax = plt.subplot(nrows, ncols, i)
            
            try:
                # Prétraiter le texte juste avant la génération
                processed_text = preprocessor.normalize_text(text)
                
                wordcloud = WordCloud(
                    width=1400,
                    height=800,
                    background_color='white',
                    stopwords=preprocessor.stop_words,
                    collocations=False,
                    max_words=150,
                    min_font_size=10,
                    max_font_size=200,
                    prefer_horizontal=0.9  # Réduit les mots verticaux
                ).generate(processed_text)
                
                ax.imshow(wordcloud, interpolation='bilinear')
                ax.set_title(f'{section} - {study_name}', pad=10, fontsize=12)
                ax.axis('off')
                
            except Exception as e:
                ax.text(0.5, 0.5, f'Erreur: {str(e)}\nTexte: {text[:50]}...',
                       horizontalalignment='center',
                       verticalalignment='center',
                       fontsize=10,
                       color='red')
                ax.set_title(f'{section} - {study_name}', pad=10, fontsize=12)
                ax.axis('off')
        
        plt.tight_layout()
        plt.savefig(f'{output_dir}/wordcloud_{section.lower()}.png', dpi=300, bbox_inches='tight')
        plt.close()

def main():
    print("Début de la génération des nuages de mots...")
    
    # Chemin vers votre fichier pré-traité
    json_file = "/home/loris/Stage/STAGE/Test/db_sortie_block/DOC/grouped_titles2.json"
    
    studies = load_data(json_file)
    generate_wordclouds(studies)
    
    print(f"\nNuages de mots générés et sauvegardés dans : {output_dir}")

if __name__ == "__main__":
    main()