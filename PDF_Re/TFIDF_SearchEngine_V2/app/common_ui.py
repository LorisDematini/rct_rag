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
from config.paths import SECTIONS_JSON_PATH, PDF_FOLDER

#Chargment unique du fichier summary.json 
with open(SECTIONS_JSON_PATH, "r", encoding="utf-8") as f:
    summary_data = json.load(f)

#Fonction de surlignage
def highlight_text(text, keywords):
    for word in sorted(keywords, key=len, reverse=True):
        pattern = re.compile(rf"(\b{re.escape(word)}\b)", flags=re.IGNORECASE)
        text = pattern.sub(r"<mark>\1</mark>", text)
    return text

def find_pdf_file(study_id, folder=PDF_FOLDER):
    for filename in os.listdir(folder):
        if study_id.lower() in filename.lower() and filename.lower().endswith(".pdf"):
            return os.path.join(folder, filename)
    return None

def display_sparse_results(results, query, top_terms_by_study=None):
    keywords = query.split()
    total_results = len(results)
    total_studies = len(summary_data)  # Nombre total d'études dans le JSON

    st.subheader(f"{total_results} / {total_studies} résultats trouvés")

    if not results:
        st.info("Aucun résultat pertinent trouvé.")
        return

    top_score = results[0]["score"] if results[0]["score"] > 0 else 1e-10

    for result in results:
        study_id = result["study_id"]
        score = result["score"]
        normalized_score = (score / top_score) * 100

        st.markdown(f"### {study_id} — Score : `{normalized_score:.2f}%`")

        #Top mots-clés
        if top_terms_by_study and study_id in top_terms_by_study:
            terms = top_terms_by_study[study_id]
            formatted_terms = ", ".join(f"**{term}** (`{score:.2f}`)" for term, score in terms)
            st.markdown(f"**Mots importants** : {formatted_terms}")

        with st.expander("Afficher les détails de l’étude"):
            if study_id not in summary_data:
                st.warning("Aucune donnée trouvée dans le fichier summary.json pour cette étude.")
                continue

            # Affichage du bouton PDF
            pdf_path = find_pdf_file(study_id)
            if pdf_path:
                with open(pdf_path, "rb") as file:
                    st.download_button(
                        label="📄 Télécharger le rapport (.pdf)",
                        data=file,
                        file_name=os.path.basename(pdf_path),
                        mime="application/pdf"
                    )
            else:
                st.info("Aucun fichier .pdf disponible pour cette étude.")

            #Affichage des sections depuis le JSON structuré
            study_content = summary_data[study_id]

            if isinstance(study_content, dict):
                for section_title, section_paragraphs in study_content.items():
                    #On retire les sections vides
                    if not section_paragraphs:
                        continue
                    col1, col2 = st.columns([1, 4])
                    with col1:
                        st.markdown(f"**{section_title}**")

                    with col2:
                        if isinstance(section_paragraphs, list):
                            for paragraph in section_paragraphs:
                                if isinstance(paragraph, str):
                                    highlighted = highlight_text(paragraph, keywords)
                                    st.markdown(highlighted, unsafe_allow_html=True)
                                else:
                                    st.markdown("Paragraphe non textuel.")
                        else:
                            st.markdown("Section invalide ou vide.")
            else:
                st.warning("Format inattendu pour cette étude.")
