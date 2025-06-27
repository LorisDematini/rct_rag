"""
Interface principale Streamlit permettant de choisir entre deux moteurs de recherche :
- Mot Clé : recherche basée sur un embedding TF-IDF et similarité cosinus
- Exacte : recherche basée sur des mots exactes et CTRL+F

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
from app.exact_app import run_exacte_app
from app.liste_app import run_liste_app

st.set_page_config(layout="wide")
st.sidebar.title("Choisissez le moteur de recherche")
mode = st.sidebar.radio("Mode", ["Similarité", "Mot-Clé", "Base de Données"])

if mode == "Similarité":
    run_sparse_app()
elif mode == "Mot-Clé":
    run_exacte_app()
else:
    run_liste_app()