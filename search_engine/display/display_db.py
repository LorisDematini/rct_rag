import os
import streamlit as st

from .display_utils import find_pdf_file
from config import download_label, show_section, no_protocol_name, no_pdf_avail, format_protocol, no_text_p


def display_list(summary : str, query: str = None) -> None:
    """
    Display a list of clinical protocols, optionally filtered by a search query.

    Args:
        summary(str): Text from summary.json, file containing all pdf extracted 
        without preprocessing.
        query (str, optional): Text input from the user to filter protocol IDs.
                               If None or empty, the full list is shown.
    """
    # If no query is provided, show the full list
    if query is None or query.strip() == "":
        st.subheader(f"Complete list of {len(summary)} protocols")
        filtered_summary = summary.items()
    else:
        # Normalize query for case-insensitive comparison
        query = query.strip().lower()
        filtered_summary = [
            (study_id, study_content)
            for study_id, study_content in summary.items()
            if query in study_id.lower()
        ]

        # If nothing matches the query
        if not filtered_summary:
            st.warning(no_protocol_name)
            return

    # Loop through all matching protocols
    for study_id, study_content in filtered_summary:
        # Remove any suffix after the first slash in study_id
        study_id = study_id.split("/", 1)[0]
        st.markdown(f"### {study_id}")

        # Try to locate the corresponding PDF file
        pdf_path = find_pdf_file(study_id)
        if pdf_path:
            # If PDF exists, show download button
            with open(pdf_path, "rb") as file:
                st.download_button(
                    label= download_label,
                    data=file,
                    file_name=os.path.basename(pdf_path),
                    mime="application/pdf"
                )
        else:
            st.info(no_pdf_avail)

        # Expandable section for detailed content
        with st.expander(show_section):
            if isinstance(study_content, dict):
                # Loop through all sections of the protocol
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
                            st.markdown(no_text_p)
            else:
                st.warning(format_protocol)
