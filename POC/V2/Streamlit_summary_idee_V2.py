import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import json
import re

# --- Chargement des JSONs ---
preprocessed_path = "/home/loris/Stage/STAGE/Test/db_sortie_block/DOC/Summary/Propre/summary_preprocessed.json"
original_path = "/home/loris/Stage/STAGE/Test/db_sortie_block/DOC/Summary/Comparaison/summary-title.json"

with open(preprocessed_path, "r", encoding="utf-8") as f:
    preprocessed_data = json.load(f)

with open(original_path, "r", encoding="utf-8") as f:
    original_data = json.load(f)


# Fonction de surlignage
def surligne(text, words):
    for word in sorted(words, key=len, reverse=True):  # pour éviter les conflits type "digit" vs "digits"
        word_regex = re.compile(rf"(\b{re.escape(word)}\b)", flags=re.IGNORECASE)
        text = word_regex.sub(r"<mark>\1</mark>", text)
    return text

# --- Création des documents ---
docs = []
for key, value in preprocessed_data.items():
    if "Summary" in value and key in original_data and "Summary" in original_data[key]:
        docs.append({
            "title": key,
            "preprocessed": value["Summary"],
            "original": original_data[key]["Summary"]
        })

st.title("🔍 Moteur de recherche dans les résumés (affichage texte original)")

if not docs:
    st.warning("Aucun champ 'Summary' trouvé dans les données.")
else:
    texts = [doc["preprocessed"] for doc in docs]
    titles = [doc["title"] for doc in docs]

    # --- TF-IDF ---
    vectorizer = TfidfVectorizer(max_df=0.95)
    tfidf_matrix = vectorizer.fit_transform(texts)

    # --- Interface utilisateur ---
    query = st.text_input("Entrez votre requête")

    if query:
        query_vec = vectorizer.transform([query])
        similarities = cosine_similarity(query_vec, tfidf_matrix).flatten()
        sorted_indices = np.argsort(similarities)[::-1]

        st.subheader("📄 Résultats les plus pertinents")
        for idx in sorted_indices[:10]:  # Top 10
            if similarities[idx] > 0:
                st.markdown(f"**{titles[idx]}** — Similarité : `{similarities[idx]:.4f}`")
                with st.expander("Afficher le texte original"):
                    # Surligner les mots de la requête dans le texte
                    query_words = query.lower().split()
                    original_text = docs[idx]["original"]
                    highlighted_text = surligne(original_text, query_words)
                    st.markdown(highlighted_text, unsafe_allow_html=True)
            else:
                break
