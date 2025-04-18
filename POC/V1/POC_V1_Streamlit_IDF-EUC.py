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
    print("\n------ VECTEUR DE LA REQUÊTE ------")
    print(f"Requête : '{query}'")
    print("Vecteur sparse (non zéros) :")
    query_sparse = query_vector.tocoo()
    for i, j, v in zip(query_sparse.row, query_sparse.col, query_sparse.data):
        print(f"  Mot index {j} (valeur TF-IDF : {v:.4f})")
    print("Shape du vecteur dense :", query_vector.shape)
    print("Norme L2 du vecteur requête :", (query_vector @ query_vector.T)[0, 0]**0.5)
    print("-----------------------------------\n")

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
    print("------ TF-IDF INFO ------")
    print(f"Nombre total de documents (sections) : {len(texts)}")
    print(f"Nombre de mots uniques (vocabulaire) : {len(vectorizer.vocabulary_)}")
    print("Exemples de mots du vocabulaire :")
    for i, (word, idx) in enumerate(vectorizer.vocabulary_.items()):
        if i >= 10:
            break
        print(f"  {word} => index {idx}")
    print("Shape de la matrice TF-IDF :", tfidf_matrix.shape)  # (n_documents, n_mots)
    print("--------------------------\n")


#Query
query = st.text_input("Entrez votre requête :", "")

if query:
    with st.spinner("Recherche en cours..."):
        results = search(query, vectorizer, tfidf_matrix, labels)
        st.subheader("Résultats de la recherche :")
        for (study_id, section, content), dist in results:
            with st.expander(f"Étude : {study_id} | Section : {section} | Distance : {dist:.4f}"):
                st.write(content)
