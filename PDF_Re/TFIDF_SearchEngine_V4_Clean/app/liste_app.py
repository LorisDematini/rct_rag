#liste_app.py

from display.display_utils import title_print, text_input
from display.display_list import display_liste

def run_liste_app():
    
    texte = "Base de données des protocoles"
    title_print(texte)

    texte2 = "Entrez le protocole voulu"
    query = text_input(texte2)

    display_liste(query)
