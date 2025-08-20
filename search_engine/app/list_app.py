'''
liste_app.py

This module runs the Streamlit application to access the list of clinical trials.

Main function: `run_list_app()`

Functionality:
1. Displays a title.
2. Load summary data to show all of the content
2. Provides a text input field to filter displayed protocols by their name.
3. Dynamically shows the list of matching protocols via `display_list(query)`.

This mode allows free navigation through documents, with or without a query.
'''

from display import title_print, text_input, display_list
from config import title_data
from core import load_list

# Main function
def run_list_app():
    
    title_print(title_data)

    summary = load_list()

    query_list = text_input()

    # Display the list of clinical trials with or without a query
    display_list(summary, query_list)
