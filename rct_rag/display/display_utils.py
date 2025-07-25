"""
display_utils.py

Ce module contient des fonctions utilitaires pour :
- Charger les fichiers JSON contenant les résumés, sections et métadonnées.
- Extraire et nettoyer les identifiants d'étude pour retrouver les fichiers PDF associés.
- Afficher les éléments de l'interface utilisateur avec Streamlit (titres, radios, input, spinner, etc.).

Fonctions principales :
- get_summary_data(), get_summary_data_full(), get_summary_list() : chargent les différents jeux de données.
- find_pdf_file() : cherche un fichier PDF correspondant à un study_id.
- clean_string() : standardise une chaîne de caractères (pour retrouver les noms).
- Fonctions d'interface (Streamlit) : set_page(), sidebar_title(), title_print(), sidebar_radio(), etc.
"""

import os
import json
from config.paths import SECTIONS_JSON_PATH, SECTIONS_FULL_JSON_PATH, SUMMARY_JSON_PATH, PDF_FOLDER
import streamlit as st

#Chargement des différents fichiers pour les moteurs
with open(SECTIONS_JSON_PATH, "r", encoding="utf-8") as f:
    summary_data = json.load(f)

with open(SECTIONS_FULL_JSON_PATH, "r", encoding="utf-8") as f:
    summary_data_full = json.load(f)

with open(SUMMARY_JSON_PATH, "r", encoding="utf-8") as f:
    summary = json.load(f)

def get_summary_data():
    return summary_data

def get_summary_data_full():
    return summary_data_full

def get_summary_list():
    return summary

#Mini Preprocess pour trouver le nom de l'étude dans la fonction find_pdf_file
def clean_string(s):
    return s.lower().replace("-", " ").replace("_", " ").replace("/", " ").strip()

#Cherche le nom de l'étude dans les fichiers PDF
def find_pdf_file(study_id, folder=PDF_FOLDER):
    study_id_clean = clean_string(study_id)

    for filename in os.listdir(folder):
        if not filename.lower().endswith(".pdf"):
            continue
        fname_clean = clean_string(filename)
        if fname_clean.startswith(study_id_clean) or study_id_clean in fname_clean:
            return os.path.join(folder, filename)
    return None

#Fonctions de display
def set_page(): 
    st.set_page_config(layout="wide")

def sidebar_title(txt):
    st.sidebar.title(txt)

def title_print(txt):
    st.title(txt)

def sidebar_radio(liste_txt):
    mode = st.sidebar.radio("Mode", liste_txt)
    return mode

def spinner_context(message="Chargement des données ..."):
    return st.spinner(message)

def text_input(texte="Entrez votre requête"):
    input = st.text_input(texte)
    return input
    
def radio_button(message, liste_options):
    selected = st.radio(message, liste_options, horizontal=True)
    return selected