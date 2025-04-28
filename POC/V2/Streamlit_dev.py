import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import numpy as np
import json

# --- Chargement des données JSON ---
st.title("🔎 Moteur de recherche TF-IDF (depuis un JSON)")
json_file = st.file_uploader("Uploader un fichier JSON", type="json")

if json_file:
    data = json.load(json_file)
    docs = [{"title": key, "text": value["Summary"]} for key, value in data.items() if "Summary" in value]

    if not docs:
        st.warning("Aucun champ 'Summary' trouvé dans les données.")
    else:
        # --- Préparation du corpus ---
        texts = [doc["text"] for doc in docs]
        titles = [doc["title"] for doc in docs]

        # --- TF-IDF ---
        vectorizer = TfidfVectorizer(max_df=0.99)
        tfidf_matrix = vectorizer.fit_transform(texts)
        vocab = vectorizer.vocabulary_
        idf_vals = dict(zip(vectorizer.get_feature_names_out(), vectorizer.idf_))

        # --- Interface de recherche ---
        query = st.text_input("Entrez votre requête", "Votre requête ici")

        if query:
            # Vectorisation de la requête
            query_vec = vectorizer.transform([query])
            similarities = cosine_similarity(query_vec, tfidf_matrix).flatten()
            sorted_indices = np.argsort(similarities)[::-1]

            st.subheader("📊 Résultats de la recherche")
            for idx in sorted_indices:
                st.markdown(f"**{titles[idx]}** — Similarité : `{similarities[idx]:.4f}`")
                with st.expander("Afficher le texte"):
                    st.write(docs[idx]["text"])

            # --- Mode développeur ---
            st.markdown("---")
            st.subheader("🧠 Mode développeur")

            # Vocabulaire
            st.markdown("**📚 Vocabulaire et index TF-IDF :**")
            vocab_df = pd.DataFrame(sorted([(word, idx) for word, idx in vocab.items()]), columns=["Mot", "Index"])
            st.dataframe(vocab_df, use_container_width=True)

            # Matrice TF-IDF
            st.markdown("**🧮 Matrice TF-IDF**")
            tfidf_df = pd.DataFrame(
                tfidf_matrix.toarray().astype(float),
                columns=vectorizer.get_feature_names_out(),
                index=titles
            )
            st.dataframe(tfidf_df.style.format("{:.2f}"), use_container_width=True)

            # Vecteur de la requête
            st.markdown("**🧾 Vecteur TF-IDF de la requête**")
            query_array = query_vec.toarray()[0]
            non_zero_query = [(vectorizer.get_feature_names_out()[i], query_array[i])
                              for i in range(len(query_array)) if query_array[i] > 0]
            query_df = pd.DataFrame(non_zero_query, columns=["Mot", "Poids TF-IDF"])
            query_df["Poids TF-IDF"] = pd.to_numeric(query_df["Poids TF-IDF"], errors="coerce")
            query_df = query_df.dropna(subset=["Poids TF-IDF"])
            st.dataframe(query_df.style.format({"Poids TF-IDF": "{:.4f}"}), use_container_width=True)

            # Valeurs IDF
            st.markdown("**ℹ️ Valeurs IDF du vocabulaire :**")
            idf_df = pd.DataFrame(list(idf_vals.items()), columns=["Mot", "IDF"])
            idf_df["IDF"] = pd.to_numeric(idf_df["IDF"], errors="coerce")
            st.dataframe(idf_df.sort_values(by="IDF", ascending=False).reset_index(drop=True)
                         .style.format({"IDF": "{:.4f}"}), use_container_width=True)
