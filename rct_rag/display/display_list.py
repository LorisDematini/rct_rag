"""
display_list.py

Module d'affichage de la liste des protocoles disponibles dans l'application Streamlit.

Fonction principale :
- display_liste(query=None) :
    Affiche tous les protocoles sous forme de liste.
    - Si `query` est vide, tous les protocoles sont listés.
    - Si `query` est renseignée, les IDs sont filtrés en fonction de la requête utilisateur.

Fonctionnalités :
- Affichage du titre de chaque protocole (study_id).
- Téléchargement du rapport PDF associé.
- Affichage du contenu structuré du protocole via un expander.
- Gestion de contenu inattendu ou vide avec messages Streamlit.
"""


import os
import streamlit as st

from display.display_utils import find_pdf_file, get_summary_list

#texte de base
summary = get_summary_list()

#Affiche l'entièreté des PDF ou filtre avec une requête
def display_liste(query=None):
    #Filtre les protocoles affichés en fonction de la requête
    if query is None or query.strip() == "":
        st.subheader(f"Liste complète des {len(summary)} protocoles")
        filtered_summary = summary.items()
    else:
        query = query.strip().lower()
        filtered_summary = [
            (study_id, study_content)
            for study_id, study_content in summary.items()
            if query in study_id.lower()
        ]

        if not filtered_summary:
            st.warning("Aucun protocole trouvé avec ce nom.")
            return

    #Affiche les PDF choisis sous forme de texte extrait d'un JSON, avec un téléchargement du PDF
    for study_id, study_content in filtered_summary:
        st.markdown(f"### {study_id}")

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
            st.info("Aucun fichier .pdf disponible pour cette protocole.")

        with st.expander("Afficher le contenu de protocole"):
            if isinstance(study_content, dict):
                for section_title, section_paragraphs in study_content.items():
                    if not section_paragraphs:
                        continue
                    col1, col2 = st.columns([1, 4])
                    with col1:
                        st.markdown(f"**{section_title}**")
                    with col2:
                        if isinstance(section_paragraphs, str):
                            st.markdown(section_paragraphs)
                        else:
                            st.markdown("Paragraphe non textuel.")
            else:
                st.warning("Format inattendu pour ce protocole.")
