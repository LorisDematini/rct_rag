"""
common_ui.py

Ce module contient les fonctions d'affichage pour l'interface utilisateur Streamlit 
du moteur de recherche, à la fois pour les recherches par similarité sémantique dense 
et pour les recherches lexicales sparse.

Fonctions :
- highlight_text(text, keywords) : Surligne les mots-clés dans un texte donné en utilisant des balises HTML <mark>.
- display_sparse_results(results, query) : Affiche les résultats d'une recherche sparse sous forme de tableau avec surlignage des mots-clés.
- display_dense_results(results, query, study_sections) : Affiche les résultats d'une recherche dense (par embeddings), triés par pertinence.

"""

from collections import defaultdict
import streamlit as st
import re
import json
from config.paths import RAW_JSON_PATH

# --- Chargement unique du fichier summary.json ---
with open(RAW_JSON_PATH, "r", encoding="utf-8") as f:
    summary_data = json.load(f)

# --- Fonction de surlignage ---
def highlight_text(text, keywords):
    for word in sorted(keywords, key=len, reverse=True):
        pattern = re.compile(rf"(\b{re.escape(word)}\b)", flags=re.IGNORECASE)
        text = pattern.sub(r"<mark>\1</mark>", text)
    return text

def display_sparse_results(results, query):
    keywords = query.split()
    st.subheader("Résultats les plus pertinents")

    if not results:
        st.info("Aucun résultat pertinent trouvé.")
        return

    top_score = results[0]["score"] if results[0]["score"] > 0 else 1e-10

    for result in results:
        study_id = result["study_id"]
        score = result["score"]
        normalized_score = (score / top_score) * 100

        st.markdown(f"### {study_id} — Score : `{normalized_score:.2f}%`")

        with st.expander("Afficher les détails de l’étude"):
            if study_id not in summary_data:
                st.warning("Aucune donnée trouvée dans le fichier summary.json pour cette étude.")
                continue

            study_content = summary_data[study_id]

            for i, section in enumerate(study_content):
                if isinstance(section, list) and len(section) == 2:
                    section_title, section_text = section
                    col1, col2 = st.columns([1, 4])
                    with col1:
                        st.markdown(f"**{section_title}**")
                    with col2:
                        highlighted = highlight_text(section_text, keywords)
                        st.markdown(highlighted, unsafe_allow_html=True)
                else:
                    st.markdown(f"Section {i + 1} : {str(section)}")

def display_dense_results(results, query, study_sections):
    st.subheader("Résultats les plus pertinents")

    if not results:
        st.info("Aucun résultat pertinent trouvé.")
        return

    # Calcul du top score global (pour normalisation)
    top_score = max(
        max(section["score"] for section in sections)
        for sections in results.values()
    )
    if top_score <= 1e-6:
        top_score = 1e-6

    # Parcours des études triées par score décroissant
    for study_id, sections in sorted(
        results.items(),
        key=lambda item: max(section["score"] for section in item[1]),
        reverse=True
    ):
        best_score = max(section["score"] for section in sections)
        normalized_score = (best_score / top_score) * 100

        st.markdown(f"### {study_id} — Score : `{normalized_score:.2f}%`")

        with st.expander("Afficher un extrait du contenu"):
            if study_id not in study_sections:
                st.warning(f"Aucune donnée trouvée dans le JSON dense pour l'étude `{study_id}`.")
                continue

            # Dictionnaire pour accéder rapidement aux scores par texte
            score_by_text = {s["text"].strip(): s["score"] for s in sections}

            # Trouver le texte ayant le meilleur score
            best_section_text = max(score_by_text.items(), key=lambda x: x[1])[0]

            # Afficher les sections de l'étude sans surlignage
            for section in study_sections[study_id]:
                section_title = section["field"]
                section_text = section["text"]

                col1, col2 = st.columns([1, 4])
                with col1:
                    # Affiche le score si c'est la section la plus pertinente
                    if section_text.strip() == best_section_text:
                        section_score = score_by_text[best_section_text]
                        st.markdown(f"**{section_title}** — Score : `{section_score:.2f}`")
                    else:
                        st.markdown(f"**{section_title}**")
                with col2:
                    st.markdown(section_text)