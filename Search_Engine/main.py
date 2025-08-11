import sys
# Prevent Streamlit from scanning this special torch module
import types
sys.modules['torch.classes'] = types.ModuleType('torch.classes')

from app import run_sparse_app, run_list_app, run_exact_app
from display import set_page, sidebar_title, sidebar_radio
from config import title_main

set_page()

sidebar_title(title_main)

mode = sidebar_radio()

if mode == "Similarity":
    run_sparse_app()
elif mode == "Key-Words":
    run_exact_app()
else:
    run_list_app()
