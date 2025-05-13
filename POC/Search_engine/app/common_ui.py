# app/common_ui.py
from sklearn.base import defaultdict
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

def display_results(results, query):
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

            if isinstance(study_content, list):  # ancien format : liste de [titre, contenu]
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

            elif isinstance(study_content, dict):  # format dict {titre: contenu}
                for section_title, section_text in study_content.items():
                    col1, col2 = st.columns([1, 4])
                    with col1:
                        st.markdown(f"**{section_title}**")
                    with col2:
                        if isinstance(section_text, str):
                            highlighted = highlight_text(section_text, keywords)
                            st.markdown(highlighted, unsafe_allow_html=True)
                        else:
                            st.markdown(str(section_text))

def display_embedding_results(results, query, summary_data):
    keywords = query.split()
    st.subheader("Résultats les plus pertinents")

    if not results:
        st.info("Aucun résultat pertinent trouvé.")
        return

    # Calcul du top score global
    top_score = max(
        max(section["score"] for section in sections)
        for sections in results.values()
    )
    if top_score <= 1e-6:
        top_score = 1e-6

    for study_id, sections in sorted(
        results.items(),
        key=lambda item: max(section["score"] for section in item[1]),
        reverse=True
    ):
        best_score = max(section["score"] for section in sections)
        normalized_score = (best_score / top_score) * 100

        st.markdown(f"### {study_id} — Score : `{normalized_score:.2f}%`")

        with st.expander("Afficher un extrait du contenu"):
            if study_id not in summary_data:
                st.warning("Aucune donnée trouvée dans le fichier summary.json pour cette étude.")
                continue

            study_content = summary_data[study_id]

            if isinstance(study_content, list):
                for section in study_content:
                    if isinstance(section, list) and len(section) == 2:
                        section_title, section_text = section
                        section_score = next(
                            (s["score"] for s in sections if section_text.strip() in s["text"].strip()),
                            0
                        )
                        col1, col2 = st.columns([1, 4])
                        with col1:
                            st.markdown(f"**{section_title}** - Score : `{section_score:.2f}`")
                        with col2:
                            st.markdown(section_text)
