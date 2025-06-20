"""
Interface principale Streamlit permettant de choisir entre deux moteurs de recherche :
- Sparse : recherche basée sur un embedding TF-IDF et similarité cosinus
- Dense : recherche basée sur embeddings HuggingFace et index FAISS

Le module spécial 'torch.classes' est bypassé pour éviter des conflits lors du scan par Streamlit.
"""

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import types

# Empêche Streamlit de scanner ce module spécial de torch
sys.modules['torch.classes'] = types.ModuleType('torch.classes')
import streamlit as st
from app.sparse_app import run_sparse_app

st.set_page_config(layout="wide")
run_sparse_app()