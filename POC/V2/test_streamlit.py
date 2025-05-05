import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import json

# --- Chargement du JSON ---
json_path = "/home/loris/Stage/STAGE/Test/db_sortie_block/DOC/Summary/Comparaison/summary-title.json"
with open(json_path, "r", encoding="utf-8") as f:
    data = json.load(f)

# --- Préparation des documents ---
docs = [{"title": key, "text": value["Summary"]} for key, value in data.items() if "Summary" in value]

st.title("Moteur de recherche dans les résumés")

if not docs:
    st.warning("Aucun champ 'Summary' trouvé dans les données.")
else:
    texts = [doc["text"] for doc in docs]
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
        for idx in sorted_indices[:10]:  # Affiche les 10 meilleurs résultats
            if similarities[idx] > 0:
                st.markdown(f"**{titles[idx]}** — Similarité : `{similarities[idx]:.4f}`")
                with st.expander("Afficher le texte"):
                    st.write(docs[idx]["text"])
            else:
                break