import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Empêche Streamlit de scanner ce module spécial de torch
import types
sys.modules['torch.classes'] = types.ModuleType('torch.classes')

from app.sparse_app import run_sparse_app
from app.exact_app import run_exacte_app
from app.liste_app import run_liste_app
from display.display_utils import set_page, sidebar_title, sidebar_radio

set_page()

titre= "Choisissez le moteur de recherche"
sidebar_title(titre)

liste_sous_titre = ["Similarité", "Mot-Clé", "Base de Données"]

mode = sidebar_radio(liste_sous_titre)

if mode == "Similarité":
    run_sparse_app()
elif mode == "Mot-Clé":
    run_exacte_app()
else:
    run_liste_app()
