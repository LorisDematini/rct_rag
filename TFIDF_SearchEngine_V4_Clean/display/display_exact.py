import streamlit as st
import os
from display.highlight import highlight_text_exact
from display.display_utils import find_pdf_file, get_summary_data_full
from core.exact_search import parse_query

summary_data_full = get_summary_data_full()

def display_exacte_results(results, query, selected_section=None):
    parsed = parse_query(query)
    mode = parsed["operator"]

    unique_study_ids = {res["study_id"] for res in results}
    total_results = len(unique_study_ids)
    total_studies = len(summary_data_full)

    if selected_section == "Toutes les sections":
        st.subheader(f"{total_results} / {total_studies} protocole(s) trouvé(s)")
    else:
        st.subheader(f"{len(results)} section(s) trouvée(s)")

    if not results:
        st.info("Aucun protocole pertinent trouvé.")
        return

    display_all_sections = (selected_section is None) or (selected_section == "Toutes les sections")

    if display_all_sections:
        results_by_study = {}
        for res in results:
            sid = res["study_id"]
            if sid not in results_by_study:
                results_by_study[sid] = res

        for study_id in results_by_study:
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
                st.info("Aucun fichier .pdf disponible pour ce protocole.")

            study_content = summary_data_full.get(study_id, {})
            if not isinstance(study_content, dict):
                st.warning("Format inattendu pour ce protocole.")
                continue

            with st.expander("Afficher toutes les sections"):
                for sec, paragraphs in study_content.items():
                    if not paragraphs:
                        continue
                    col1, col2 = st.columns([1, 4])
                    with col1:
                        st.markdown(f"**{sec}**")
                    with col2:
                        for paragraph in paragraphs:
                            if isinstance(paragraph, str):
                                highlighted = highlight_text_exact(paragraph, query, mode)
                                st.markdown(highlighted, unsafe_allow_html=True)
                            else:
                                st.markdown("Paragraphe non textuel.")
    else:
        for res in results:
            study_id = res["study_id"]
            section_name = res.get("section_name", "UNKNOWN")
            st.markdown(f"### {study_id} — Section : {section_name}")

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
                st.info("Aucun fichier .pdf disponible pour ce protocole.")

            study_content = summary_data_full.get(study_id, {})
            section_paragraphs = study_content.get(section_name, [])

            col1, col2 = st.columns([1, 4])
            with col1:
                st.markdown(f"**{section_name}**")
            with col2:
                for paragraph in section_paragraphs:
                    if isinstance(paragraph, str):
                        highlighted = highlight_text_exact(paragraph, query, mode)
                        st.markdown(highlighted, unsafe_allow_html=True)
                    else:
                        st.markdown("Paragraphe non textuel.")
