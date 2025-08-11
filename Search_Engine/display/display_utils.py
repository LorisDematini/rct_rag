import os
import json
from config import SECTIONS_JSON_PATH, PDF_FOLDER, SECTIONS_FULL_JSON_PATH, type_query, options_radio, title_main
import streamlit as st
from typing import Any, Optional, Dict, List

# Load data once on import
with open(SECTIONS_JSON_PATH, "r", encoding="utf-8") as f:
    summary_data: Dict[str, Any] = json.load(f)

with open(SECTIONS_FULL_JSON_PATH, "r", encoding="utf-8") as f:
    summary_data_full = json.load(f)


def get_summary_data() -> Dict[str, Any]:
    """
    Return the summary data dictionary loaded from sections JSON.
    """
    return summary_data

def get_summary_data_full() -> Dict[str, Any]:
    """Return the full summary data dictionary (if needed)."""
    return summary_data_full


def extract_top_terms_by_study(top_terms: Dict[str, Any]) -> Dict[str, Any]:
    """
    Return a dictionary of top terms keyed by study ID.
    """
    return {study: terms for study, terms in top_terms.items()}

def clean_string(s: str) -> str:
    """
    Normalize a string for matching by lowercasing and replacing some separators.
    """
    return s.lower().replace("-", " ").replace("_", " ").replace("/", " ").strip()

def find_pdf_file(study_id: str, folder: str = PDF_FOLDER) -> Optional[str]:
    """
    Search for a PDF file in the given folder matching the study_id.
    """
    study_id_clean = clean_string(study_id)

    for filename in os.listdir(folder):
        if not filename.lower().endswith(".pdf"):
            continue
        fname_clean = clean_string(filename)
        if fname_clean.startswith(study_id_clean) or study_id_clean in fname_clean:
            return os.path.join(folder, filename)
    return None

def set_page() -> None:
    """
    Configure the Streamlit page layout as wide.
    """
    st.set_page_config(layout="wide")

def sidebar_title() -> None:
    """
    Display a title in the Streamlit sidebar.
    """
    st.sidebar.title(title_main)

def title_print(txt: str) -> None:
    """
    Display a main title in the Streamlit app.
    """
    st.title(txt)

def sidebar_radio() -> str:
    """
    Display a radio button selection in the sidebar.
    """
    mode = st.sidebar.radio("Mode", options_radio)
    return mode

def text_input(prompt: str = type_query) -> str:
    """
    Display a Streamlit text input box.
    """
    return st.text_input(prompt)

def radio_button(label: str, options: List[str]) -> str:
    """
    Display a horizontal Streamlit radio button group.
    """
    return st.radio(label, options, horizontal=True)
