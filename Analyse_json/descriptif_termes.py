import json
import os
import re
from collections import defaultdict
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
import matplotlib.pyplot as plt
from nltk.corpus import stopwords
import nltk

# Télécharger les stopwords
nltk.download('stopwords')

# Charger les données
with open('/home/loris/Stage/STAGE/Test/db_sortie_block/DOC/grouped_titles2.json', 'r') as file:
    data = json.load(file)

# Initialiser les stopwords
stop_words = set(stopwords.words('english'))

# 1. Regrouper le texte par section (toutes études confondues)
section_texts = defaultdict(str)

for study in data.values():
    for section, text in study.items():
        if isinstance(text, str) and text.strip():
            # Filtrer les stopwords avant l'agrégation
            words = [word for word in text.split() if word.lower() not in stop_words]
            filtered_text = ' '.join(words)
            if filtered_text.strip():
                section_texts[section] += filtered_text + " "

# 2. Analyser les fréquences par section
section_results = {}

for section, text in section_texts.items():
    if not text.strip():
        continue
        
    try:
        # Vectorisation avec stopwords déjà filtrés
        vectorizer = CountVectorizer(max_features=50, stop_words=list(stop_words))
        X = vectorizer.fit_transform([text])
        
        if X.shape[1] == 0:
            print(f"Aucun terme valide dans la section {section} - texte: '{text[:50]}...'")
            continue
            
        vocab = vectorizer.get_feature_names_out()
        counts = X.toarray()[0]
        
        section_results[section] = pd.Series(counts, index=vocab).sort_values(ascending=False)
        
    except ValueError as e:
        print(f"Erreur dans la section {section}: {str(e)}")
        continue

# 3. Sauvegarder les résultats
if section_results:
    output_dir = "/home/loris/Stage/STAGE/Test/db_sortie_block/DOC/analysis/section_term_frequency"
    os.makedirs(output_dir, exist_ok=True)

    df_sections = pd.DataFrame(section_results)
    df_sections.fillna(0, inplace=True)
    df_sections['total'] = df_sections.sum(axis=1)

    for section in df_sections.columns[:-1]:
        top_terms = df_sections[section].sort_values(ascending=False).head(20)
        
        if not top_terms.empty:
            plt.figure(figsize=(10, 6))
            top_terms.head(10).plot.barh()
            plt.title(f'Top 10 termes - {section}')
            plt.tight_layout()
            plt.savefig(f'{output_dir}/{section}_top_terms.png')
            plt.close()

    df_sections.sort_values(by='total', ascending=False).to_csv(
        f'{output_dir}/all_sections_term_frequencies.csv')
    
    print(f"Analyse terminée. Résultats sauvegardés dans : {output_dir}")
else:
    print("Aucune donnée valide après traitement - vérifiez votre fichier d'entrée")