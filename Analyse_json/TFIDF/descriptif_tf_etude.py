import json
import pandas as pd
import matplotlib.pyplot as plt
import os
import re
import unicodedata
import nltk
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer

# Téléchargements NLTK
nltk.download('stopwords')

# Configuration
output_dir = "/home/loris/Stage/STAGE/Test/db_sortie_block/DOC/analysis/TFIDF/Etude"
os.makedirs(output_dir, exist_ok=True)

class TextPreprocessor:
    def __init__(self):
        self.stop_words = list(stopwords.words('english'))
            
    def normalize_text(self, text):
        if not isinstance(text, str):
            return ""
        
        text = text.lower()
        text = unicodedata.normalize('NFKD', text).encode('ASCII', 'ignore').decode('utf-8')
        text = re.sub(r'[^\w\s]', ' ', text)
        text = re.sub(r'\s+', ' ', text).strip()
        return text

def load_and_preprocess_data(filepath):
    preprocessor = TextPreprocessor()
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    for study in data.values():
        for section in study:
            if isinstance(study[section], str):
                study[section] = preprocessor.normalize_text(study[section])
    
    return data

def build_tfidf_analysis(studies, sections=['SUMMARY','SCIENTIFIC JUSTIFICATION','OBJECTIVES','METHODOLOGY','PROCEDURE','ELIGIBILITY','DATA MANAGEMENT','STATISTICAL']):
    results = {}
    
    for section in sections:
        # Récupérer les textes pour cette section
        texts = []
        study_names = []
        for name, data in studies.items():
            if section in data and data[section].strip():
                texts.append(data[section])
                study_names.append(name)
        
        if not texts:  # Si pas de textes valides
            print(f"\n--- Section {section} ---")
            print("Aucun texte valide trouvé")
            continue
            
        # Créer le vectoriseur TF-IDF
        vectorizer = TfidfVectorizer(
            stop_words='english',
            max_df=0.9,
            min_df=2,
            lowercase=True
        )
        
        try:
            X_mat = vectorizer.fit_transform(texts)
            word_counts = X_mat.sum(axis=0).A1
            vocab = vectorizer.get_feature_names_out()
            word_freq = pd.DataFrame({'word': vocab, 'tfidf': word_counts}).sort_values(by='tfidf', ascending=False)
            
            # Sauvegarder les résultats
            results[section] = {
                'vectorizer': vectorizer,
                'matrix': X_mat,
                'frequencies': word_freq
            }
            
            # Visualisation
            plt.figure(figsize=(10, 6))
            word_freq.head(20).plot.bar(x='word', y='tfidf', legend=False)
            plt.title(f"Top 20 termes TF-IDF - {section}")
            plt.xlabel("Terme")
            plt.ylabel("Somme TF-IDF")
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.savefig(f'{output_dir}/tfidf_top_terms_{section.lower()}.png')
            plt.close()
            
            # Sauvegarder les fréquences en CSV
            word_freq.to_csv(f'{output_dir}/tfidf_frequencies_{section.lower()}.csv', index=False)
            
        except ValueError as e:
            print(f"\n--- Section {section} ---")
            print(f"Erreur dans l'analyse TF-IDF: {str(e)}")
    
    return results

def main(json_file):
    print("Début de l'analyse TF-IDF...")
    
    studies = load_and_preprocess_data(json_file)
    results = build_tfidf_analysis(studies)
    
    print(f"\nAnalyse TF-IDF terminée. Résultats sauvegardés dans : {output_dir}")

if __name__ == "__main__":
    json_file = "/home/loris/Stage/STAGE/Test/db_sortie_block/DOC/grouped_titles2.json"
    main(json_file)