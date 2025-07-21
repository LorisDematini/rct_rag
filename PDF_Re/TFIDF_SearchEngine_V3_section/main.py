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