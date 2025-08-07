import sys
# Prevent Streamlit from scanning this special torch module
import types
sys.modules['torch.classes'] = types.ModuleType('torch.classes')

from app import run_sparse_app, run_list_app, run_exact_app
from display import set_page, sidebar_title, sidebar_radio

set_page()

title = "Choose the search engine"
sidebar_title(title)

subtitle_list = ["Similarity", "Key-Words", "Database"]

mode = sidebar_radio(subtitle_list)

if mode == "Similarity":
    run_sparse_app()
elif mode == "Key-Words":
    run_exact_app()
else:
    run_list_app()
