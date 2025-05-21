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

import os
import streamlit as st
import re
import json
from config.paths import RAW_JSON_PATH, DOCX_FOLDER

# --- Chargement unique du fichier summary.json ---
with open(RAW_JSON_PATH, "r", encoding="utf-8") as f:
    summary_data = json.load(f)

# --- Fonction de surlignage ---
def highlight_text(text, keywords):
    for word in sorted(keywords, key=len, reverse=True):
        pattern = re.compile(rf"(\b{re.escape(word)}\b)", flags=re.IGNORECASE)
        text = pattern.sub(r"<mark>\1</mark>", text)
    return text

def find_docx_file(study_id, folder=DOCX_FOLDER):
    for filename in os.listdir(folder):
        if study_id.lower() in filename.lower() and filename.lower().endswith(".docx"):
            return os.path.join(folder, filename)
    return None


def display_sparse_results(results, query, top_terms_by_study=None):
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

        # --- Affichage des top mots-clés TF-IDF ---
        if top_terms_by_study and study_id in top_terms_by_study:
            terms = top_terms_by_study[study_id]
            formatted_terms = ", ".join(f"**{term}** (`{score:.2f}`)" for term, score in terms)
            st.markdown(f"**Mots importants** : {formatted_terms}")

            with st.expander("Afficher les détails de l’étude"):
                if study_id not in summary_data:
                    st.warning("Aucune donnée trouvée dans le fichier summary.json pour cette étude.")
                    continue

                docx_path = find_docx_file(study_id)
                if docx_path:
                    with open(docx_path, "rb") as file:
                        st.download_button(
                            label="📄 Télécharger le rapport (.docx)",
                            data=file,
                            file_name=os.path.basename(docx_path),
                            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                        )
                else:
                    st.info("Aucun fichier .docx disponible pour cette étude.")

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

