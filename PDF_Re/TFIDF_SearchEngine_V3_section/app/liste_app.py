import streamlit as st
from app.common_ui import display_liste

def run_liste_app():
    st.title("Base de données des protocoles")

    query = st.text_input("Entrez le protocole voulu")

    display_liste(query)
