'''
Main.py

Application Streamlit d'un moteur de recherche dans les essais cliniques.
Il permet à l'utilisateur de choisir entre trois modes de recherche :
1. "Similarité" : recherche basée sur la similarité (TF-IDF).
2. "Mot-Clé" : recherche exacte basée sur la correspondance de mots-clés avec wildcard et opérateurs logiques.
3. "Base de Données" : affichage structuré des documents indexés, consultables manuellement.

Selon le mode sélectionné dans la barre latérale, le script appelle l'application correspondante :
- run_sparse_app() pour la recherche sémantique,
- run_exacte_app() pour la recherche par mot-clé,
- run_liste_app() pour la navigation dans la base de données.

Il configure également la page Streamlit.
'''

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

#Empêche Streamlit d'appeler ce module de torch qui crée un warning
import types
sys.modules['torch.classes'] = types.ModuleType('torch.classes')

from app.sparse_app import run_sparse_app
from app.exact_app import run_exacte_app
from app.liste_app import run_liste_app
from display.display_utils import set_page, sidebar_title, sidebar_radio

#Voir le dossier display, appel d'une fonction pour la mise en place de la page
set_page()

#Appel d'une fonction streamlit pour la création d'un titre
titre= "Choisissez le moteur de recherche"
sidebar_title(titre)

#Radio boutons pour les différents moteurs
liste_sous_titre = ["Similarité", "Mot-Clé", "Base de Données"]
mode = sidebar_radio(liste_sous_titre)

#Appel de l'application en fonction du moteur choisi
if mode == "Similarité":
    run_sparse_app()
elif mode == "Mot-Clé":
    run_exacte_app()
else:
    run_liste_app()
    