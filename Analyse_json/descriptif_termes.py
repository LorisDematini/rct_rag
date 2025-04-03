import json
from nltk.corpus import stopwords
import nltk
import os
import re
from collections import defaultdict
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
import matplotlib.pyplot as plt

# Télécharger les stopwords
nltk.download('stopwords')

# Charger les données
with open('/home/loris/Stage/STAGE/Test/db_sortie_block/DOC/grouped_titles2.json', 'r') as file:
    data = json.load(file)

# Prétraitement du texte
def preprocess_text(text):
    if not isinstance(text, str):
        return ""
    
    text = text.lower()
    text = re.sub(r'[^\w\s]', ' ', text)
    text = re.sub(r'\d+', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

# Préparer les stopwords
stop_words = set(stopwords.words('english'))

# 1. Regrouper le texte par section (toutes études confondues)
section_texts = defaultdict(str)

for study in data.values():
    for section, paragraphs in study.items():
        # Fusionner les paragraphes en un seul texte
        merged_text = " ".join([p for p in paragraphs if isinstance(p, str)])
        if merged_text:
            section_texts[section] += preprocess_text(merged_text) + " "

# 2. Analyser les fréquences par section
section_results = {}

for section, text in section_texts.items():
    if not text.strip():
        continue
        
    # Vectorisation
    vectorizer = CountVectorizer(stop_words=list(stop_words), max_features=50)
    X = vectorizer.fit_transform([text])
    vocab = vectorizer.get_feature_names_out()
    counts = X.toarray()[0]
    
    # Stocker les résultats
    section_results[section] = pd.Series(counts, index=vocab).sort_values(ascending=False)

# 3. Sauvegarder les résultats
output_dir = "/home/loris/Stage/STAGE/Test/db_sortie_block/DOC/analysis/section_term_frequency"
os.makedirs(output_dir, exist_ok=True)

# DataFrame global
df_sections = pd.DataFrame(section_results)
df_sections.fillna(0, inplace=True)

# Ajout de la colonne 'total' (somme sur toutes les sections)
df_sections['total'] = df_sections.sum(axis=1)

# Sauvegarder les top termes par section
for section in df_sections.columns[:-1]:  # On exclut la colonne 'total' ici
    top_terms = df_sections[section].sort_values(ascending=False).head(20)
    
    # Fichier CSV
    top_terms.to_csv(f'{output_dir}/{section}_top_terms.csv', header=['count'])
    
    # Visualisation
    plt.figure(figsize=(10, 6))
    top_terms.head(10).plot.bar()
    plt.title(f'Top 10 termes - {section}')
    plt.tight_layout()
    plt.savefig(f'{output_dir}/{section}_top_terms.png')
    plt.close()

# Sauvegarder le tableau complet avec la colonne total
df_sections.sort_values(by='total', ascending=False).to_csv(f'{output_dir}/all_sections_term_frequencies.csv')

print(f"Analyse terminée. Résultats sauvegardés dans : {output_dir}")