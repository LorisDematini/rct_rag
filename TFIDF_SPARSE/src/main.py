import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Prevent Streamlit from scanning this special torch module
import types
sys.modules['torch.classes'] = types.ModuleType('torch.classes')

from app.sparse_app import run_sparse_app
from display.display_utils import set_page, sidebar_title, sidebar_radio

set_page()

title = "Choose the search engine"
sidebar_title(title)

subtitle_list = ["Similarity"]

mode = sidebar_radio(subtitle_list)

if mode == "Similarity":
    run_sparse_app()
