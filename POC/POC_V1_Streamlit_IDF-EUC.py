import json
import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import euclidean_distances

# ---------- Fonctions ----------

def load_data(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

#Sections
def extract_sections(data, sections=None):
    sections = sections or ['SUMMARY', 'SCIENTIFIC JUSTIFICATION', 'OBJECTIVES', 'METHODOLOGY',
                            'PROCEDURE', 'ELIGIBILITY', 'DATA MANAGEMENT', 'STATISTICAL']
    texts = []
    labels = []
    for study_id, study in data.items():
        for section in sections:
            if section in study and isinstance(study[section], str) and study[section].strip():
                texts.append(study[section])
                labels.append((study_id, section, study[section]))
    return labels, texts

#Matrice TF-IDF
def compute_tfidf(texts):
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(texts)
    return vectorizer, tfidf_matrix

# Système de recherche (top5)
def search(query, vectorizer, tfidf_matrix, labels):
    query_vector = vectorizer.transform([query])
    distances = euclidean_distances(query_vector, tfidf_matrix)[0]
    results = sorted(enumerate(distances), key=lambda x: x[1])
    return [(labels[i], d) for i, d in results[:5]]

# ---------- Interface Streamlit ----------

st.set_page_config(page_title="Moteur de recherche d'études", layout="wide")
st.title("Moteur de recherche d'études (TF-IDF + distance euclidienne)")

#Données
json_file_path = "/home/loris/Stage/STAGE/Test/db_sortie_block/DOC/Extract/grouped_titles_preprocessed.json"

with st.spinner("Chargement des données..."):
    data = load_data(json_file_path)
    labels, texts = extract_sections(data)
    vectorizer, tfidf_matrix = compute_tfidf(texts)

#Query
query = st.text_input("Entrez votre requête :", "")

if query:
    with st.spinner("Recherche en cours..."):
        results = search(query, vectorizer, tfidf_matrix, labels)
        st.subheader("Résultats de la recherche :")
        for (study_id, section, content), dist in results:
            with st.expander(f"Étude : {study_id} | Section : {section} | Distance : {dist:.4f}"):
                st.write(content)
