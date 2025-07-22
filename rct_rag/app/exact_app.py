#exact_app.py

from core.data_loader import load_data_exact
from preprocess.processed_exact import preprocess_query
from display.display_exact import display_exacte_results
from display.display_utils import title_print, spinner_context, text_input, radio_button
from core.exact_search import exact_search
from core.exact_builder import get_available_sections

def run_exacte_app():
    titre = "Moteur de recherche par mot-clé"
    title_print(titre)

    with spinner_context():
        documents = load_data_exact()

    all_sections = get_available_sections(documents)
    sections_options = ["Toutes les sections"] + all_sections
    selected_section = radio_button("Choisissez une section", sections_options)

    query = text_input()

    if query:
        query_cleaned = preprocess_query(query)
        selected_sections = None if selected_section == "Toutes les sections" else [selected_section]
        results = exact_search(documents, query_cleaned, selected_sections=selected_sections)
        display_exacte_results(results, query, selected_section)
