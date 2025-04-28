import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import json

# --- Chargement du JSON ---
json_path = "/home/loris/Stage/STAGE/Test/db_sortie_block/DOC/Summary/Propre/summary_preprocessed.json"
with open(json_path, "r", encoding="utf-8") as f:
    data = json.load(f)

# --- Préparation des documents ---
docs = [{"title": key, "text": value["Summary"]} for key, value in data.items() if "Summary" in value]

st.title("🔍 Moteur de recherche dans les résumés")

if not docs:
    st.warning("Aucun champ 'Summary' trouvé dans les données.")
else:
    texts = [doc["text"] for doc in docs]
    titles = [doc["title"] for doc in docs]

    # --- TF-IDF ---
    vectorizer = TfidfVectorizer(smooth_idf=False)
    tfidf_matrix = vectorizer.fit_transform(texts)
    feature_names = vectorizer.get_feature_names_out()

    # --- Statistiques sur le mot 'digit' ---
    digit_index = np.where(feature_names == 'digit')[0]
    if digit_index.size > 0:
        digit_col = tfidf_matrix[:, digit_index[0]].toarray().flatten()
        total_digit_occurrences = sum(text.count("digit") for text in texts)
        st.sidebar.markdown("### 🔢 Statistiques sur `digit`")
        st.sidebar.markdown(f"- Nombre total d’occurrences : **{total_digit_occurrences}**")
        st.sidebar.markdown(f"- TF-IDF max : **{digit_col.max():.4f}**")
        st.sidebar.markdown(f"- TF-IDF moyen : **{digit_col.mean():.4f}**")
        st.sidebar.markdown(f"- Documents contenant `digit` : **{np.count_nonzero(digit_col)} / {len(docs)}**")
    else:
        st.sidebar.markdown("Le mot `digit` n'est pas présent dans le vocabulaire.")

    # --- Interface utilisateur ---
    query = st.text_input("Entrez votre requête")

    if query:
        query_vec = vectorizer.transform([query])
        similarities = cosine_similarity(query_vec, tfidf_matrix).flatten()
        sorted_indices = np.argsort(similarities)[::-1]

        st.subheader("📄 Résultats les plus pertinents")
        for idx in sorted_indices[:10]:
            if similarities[idx] > 0:
                count_digit = texts[idx].count("digit")
                digit_tfidf = digit_col[idx] if digit_index.size > 0 else 0

                st.markdown(f"**{titles[idx]}** — Similarité : `{similarities[idx]:.4f}`")
                st.markdown(f"Occurrences de `digit` : `{count_digit}` — TF-IDF : `{digit_tfidf:.4f}`")
                with st.expander("Afficher le texte"):
                    st.write(docs[idx]["text"])
            else:
                break
