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
output_dir = "/home/loris/Stage/STAGE/Test/db_sortie_block/DOC/analysis/TFIDF/Section_Prepro"
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

def build_intersection_tfidf_analysis(studies, sections=['SUMMARY','SCIENTIFIC JUSTIFICATION','OBJECTIVES','METHODOLOGY','PROCEDURE','ELIGIBILITY','DATA MANAGEMENT','STATISTICAL']):
    print("\nAnalyse inter-section TF-IDF...\n")
    section_texts = []
    valid_sections = []
    
    for section in sections:
        all_texts = []
        for study in studies.values():
            if section in study and isinstance(study[section], str):
                all_texts.append(study[section])
        
        if all_texts:
            # Fusionner tous les textes de cette section en un seul document
            full_text = " ".join(all_texts)
            section_texts.append(full_text)
            valid_sections.append(section)
        else:
            print(f"⚠️ Section vide ou manquante : {section}")
    
    # Créer le TF-IDF sur les sections comme documents
    vectorizer = TfidfVectorizer(
        stop_words='english',
        max_df=0.9,
        min_df=2,
        lowercase=True
    )
    
    X_mat = vectorizer.fit_transform(section_texts)
    vocab = vectorizer.get_feature_names_out()
    
    # Pour chaque section-document, extraire les mots les plus importants
    for idx, section in enumerate(valid_sections):
        tfidf_scores = X_mat[idx].toarray().flatten()
        word_freq = pd.DataFrame({'word': vocab, 'tfidf': tfidf_scores})
        word_freq = word_freq[word_freq['tfidf'] > 0].sort_values(by='tfidf', ascending=False)
        
        # Sauvegarde PNG + CSV
        plt.figure(figsize=(20, 6))
        word_freq.head(20).plot.bar(x='word', y='tfidf', legend=False)
        plt.title(f"Top 20 termes caractéristiques - {section}")
        plt.xlabel("Terme")
        plt.ylabel("TF-IDF")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(f'{output_dir}/tfidf_intersection_top_{section.lower()}_prepro.png')
        plt.close()
        
        word_freq.to_csv(f'{output_dir}/tfidf_intersection_{section.lower()}_prepro.csv', index=False)
    
    print("✅ Analyse TF-IDF inter-section terminée.")


def main(json_file):
    print("Début de l'analyse TF-IDF...")
    
    studies = load_and_preprocess_data(json_file)
    build_intersection_tfidf_analysis(studies)
    
    print(f"\nAnalyse TF-IDF terminée. Résultats sauvegardés dans : {output_dir}")

if __name__ == "__main__":
    json_file = "/home/loris/Stage/STAGE/Test/db_sortie_block/DOC/grouped_titles_preprocessed.json"
    main(json_file)