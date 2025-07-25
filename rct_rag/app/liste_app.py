'''
liste_app.py

Ce module exécute l'application Streamlit pour accéder à la liste des essais cliniques.

Fonction principale : `run_liste_app()`

Fonctionnalité :
1. Affiche un titre.
2. Propose un champ de recherche textuel pour filtrer les protocoles affichés selon leur nom.
3. Affiche dynamiquement la liste des protocoles correspondants via `display_liste(query)`.

Ce mode permet de naviguer librement dans les documents, avec ou sans requête.
'''

from display.display_utils import title_print, text_input
from display.display_list import display_liste

# Fonction principale
def run_liste_app():
    
    texte = "Base de données des protocoles"
    title_print(texte)

    texte2 = "Entrez le protocole voulu"
    query = text_input(texte2)

    #On affiche la liste des essais cliniques avec ou sans query
    display_liste(query)
