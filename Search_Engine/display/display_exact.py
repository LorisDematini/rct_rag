import streamlit as st
import os
from .display_utils import find_pdf_file, get_summary_data_full
from .highlight import highlight_text_exact
from core import parse_query
from config import download_label, show_section

# Load the summary data for all protocols
summary_data_full = get_summary_data_full()

def display_exacte_results(results, query, selected_section=None):
    """
    Display the results of an exact search in the Streamlit interface.

    Args:
        results (list[dict]): List of matching results, each containing at least 'study_id' and 'section_name'.
        query (str): The user’s query string (can include logical operators).
        selected_section (str, optional): Section selected by the user. If "All sections", all sections are shown.
    """
    parsed = parse_query(query)
    mode = parsed["operator"]

    # Count unique studies found and total studies available
    unique_study_ids = {res["study_id"] for res in results}
    total_results = len(unique_study_ids)
    total_studies = len(summary_data_full)

    # Show appropriate title depending on whether a specific section is selected
    if selected_section == "All sections":
        st.subheader(f"{total_results} / {total_studies} protocol(s) found")
    else:
        st.subheader(f"{len(results)} matching section(s) found")

    if not results:
        st.info("No relevant protocols found.")
        return

    display_all_sections = (selected_section is None) or (selected_section == "All sections")

    if display_all_sections:
        # Group results by study_id to only show one match per protocol
        results_by_study = {}
        for res in results:
            sid = res["study_id"]
            if sid not in results_by_study:
                results_by_study[sid] = res

        for study_id in results_by_study:
            st.markdown(f"### {study_id}")
            pdf_path = find_pdf_file(study_id)

            # Show PDF download button if the file exists
            if pdf_path:
                with open(pdf_path, "rb") as file:
                    st.download_button(
                        label= download_label,
                        data=file,
                        file_name=os.path.basename(pdf_path),
                        mime="application/pdf"
                    )
            else:
                st.info("No .pdf file available for this protocol.")

            # Display all sections and their paragraphs for the study
            study_content = summary_data_full.get(study_id, {})
            if not isinstance(study_content, dict):
                st.warning("Unexpected format for this protocol.")
                continue

            with st.expander(show_section):
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
                                st.markdown("Non-textual paragraph.")
    else:
        # If a specific section was selected, display each matching result separately
        for res in results:
            study_id = res["study_id"]
            section_name = res.get("section_name", "UNKNOWN")
            st.markdown(f"### {study_id} — Section: {section_name}")

            pdf_path = find_pdf_file(study_id)
            if pdf_path:
                with open(pdf_path, "rb") as file:
                    st.download_button(
                        label="📄 Download report (.pdf)",
                        data=file,
                        file_name=os.path.basename(pdf_path),
                        mime="application/pdf"
                    )
            else:
                st.info("No .pdf file available for this protocol.")

            # Display only the selected section’s paragraphs
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
                        st.markdown("Non-textual paragraph.")
