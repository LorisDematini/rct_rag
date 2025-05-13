import sys
import types

# Empêche Streamlit de scanner ce module spécial de torch
sys.modules['torch.classes'] = types.ModuleType('torch.classes')
import streamlit as st
from app.tfidf_app import run_tfidf_app
from app.embedding_app import run_embedding_app

st.set_page_config(layout="wide")
st.sidebar.title("Choisissez le moteur de recherche")
mode = st.sidebar.radio("Mode", ["TF-IDF", "Sémantique"])

if mode == "TF-IDF":
    run_tfidf_app()
else:
    run_embedding_app()
