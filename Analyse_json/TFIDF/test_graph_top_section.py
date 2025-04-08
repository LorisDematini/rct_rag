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
output_dir = "/home/loris/Stage/STAGE/Test/db_sortie_block/DOC/analysis/TFIDF"
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
    
    # Collecter les textes par section
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
    
    # Récupérer les top 3 termes pour chaque section
    top_terms_by_section = {}
    for idx, section in enumerate(valid_sections):
        tfidf_scores = X_mat[idx].toarray().flatten()
        word_freq = pd.DataFrame({'word': vocab, 'tfidf': tfidf_scores})
        word_freq = word_freq[word_freq['tfidf'] > 0].sort_values(by='tfidf', ascending=False)
        
        # Prendre les 3 termes les plus significatifs
        top_terms_by_section[section] = word_freq.head(5)
        
    # Graphique avec comparaison des top 3 termes par section
    print("\nCréation du graphique des top 3 termes par section...")
    
    # Préparer les données pour le graphique
    all_words = list(set([term for section in top_terms_by_section.values() for term in section['word']]))
    df_top_terms = pd.DataFrame(index=all_words)
    
    # Remplir les données de TF-IDF pour chaque section
    for section, top_terms in top_terms_by_section.items():
        for _, row in top_terms.iterrows():
            df_top_terms.loc[row['word'], section] = row['tfidf']
    
    # Remplir les valeurs manquantes par 0
    df_top_terms = df_top_terms.fillna(0)
    
    # Graphique
    df_top_terms.plot(kind='barh', stacked=False, figsize=(14, 10), width=0.9, colormap='viridis')
    plt.title("Top 3 termes par section - Analyse TF-IDF")
    plt.xlabel("TF-IDF Score")
    plt.ylabel("Termes")
    plt.tight_layout()
    plt.legend(title='Sections')
    plt.savefig(f'{output_dir}/top_5_terms_per_section_comparison.png')
    plt.close()
    
    print("✅ Graphique des top 3 termes par section sauvegardé.")

def main(json_file):
    print("Début de l'analyse TF-IDF...\n")
    
    studies = load_and_preprocess_data(json_file)
    build_intersection_tfidf_analysis(studies)
    
    print(f"\nAnalyse TF-IDF terminée. Résultats sauvegardés dans : {output_dir}")

if __name__ == "__main__":
    json_file = "/home/loris/Stage/STAGE/Test/db_sortie_block/DOC/grouped_titles_preprocessed.json"
    main(json_file)
