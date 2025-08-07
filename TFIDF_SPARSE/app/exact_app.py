"""
exact_app.py

This module runs the Streamlit application for keyword-based exact search.

Main function: `run_exact_app()`

Workflow:
1. Displays Streamlit UI components (title and spinner).
2. Loads documents and section names using `load_exact()`.
3. Dynamically retrieves the list of available sections from the documents (e.g., Introduction, Intervention, etc.).
4. Displays a radio button allowing users to filter search by a specific section or across all sections.
5. Gets the user query, applies preprocessing (`preprocess_query_ex`), and runs the exact keyword search (`search_ex`).
6. Displays the results using `display_exacte_results`.

Note:
This search engine mimics a "Ctrl+F" style exact match — it does not compute semantic similarity.
It finds sections containing the given keywords, with optional section filtering.
"""

from core import load_exact
from preprocess import preprocess_query_ex
from display.display_utils import title_print, text_input, radio_button
from core import search_ex
from display import display_exacte_results


# Main entry point for the exact search application
def run_exact_app():
    # Title display
    title = "Search Engine by key-words"
    title_print(title)

    # Load preprocessed documents and list of available section names
    documents_exact, list_sections = load_exact()

    # Create section filter options (including "All sections")
    sections_options = ["All sections"] + list_sections
    selected_section = radio_button("Selection a section", sections_options)

    # Get user query input
    query = text_input()

    if query:
        # Preprocess the input query
        query_cleaned = preprocess_query_ex(query)

        # Determine target sections (None means all sections)
        selected_sections = None if selected_section == "All sections" else [selected_section]
        
        # Perform the exact keyword search
        results = search_ex(documents_exact, query_cleaned, selected_sections=selected_sections)
        
        # Display the search results
        display_exacte_results(results, query, selected_section)
