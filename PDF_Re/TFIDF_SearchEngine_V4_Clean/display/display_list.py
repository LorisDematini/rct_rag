import os
import streamlit as st

from display.display_utils import find_pdf_file, get_summary_list

summary = get_summary_list()

def display_liste(query=None):
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
