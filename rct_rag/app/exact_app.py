'''
exact_app.py

Ce module exécute l'application Streamlit pour la recherche exacte par mot-clé.

Fonction principale : `run_exacte_app()`

Étapes :
1. Affiche des éléments streamlit : titre et spinner.
2. Charge les documents à l'aide de `load_data_exact()`.
3. Récupère dynamiquement la liste des sections disponibles dans les documents (ex : Introduction, Intervention, etc).
4. Affiche un bouton radio permettant de filtrer la recherche sur une section spécifique ou toutes les sections.
5. Récupère la requête de l'utilisateur, la prétraite (`preprocess_query`), puis lance la recherche exacte (`exact_search`).
6. Affiche les résultats via `display_exacte_results`.

Ce moteur repose sur une recherche exacte à la manière d'un ctrl+f : il ne calcule pas de similarité, mais identifie les sections contenant les mots-clés donnés, avec ou sans options de filtrage par section.
'''

from core.data_loader import load_data_exact
from preprocess.processed_exact import preprocess_query
from display.display_exact import display_exacte_results
from display.display_utils import title_print, spinner_context, text_input, radio_button
from core.exact_search import exact_search
from core.exact_builder import get_available_sections

#Fonction principale 
def run_exacte_app():

    #Titre
    titre = "Moteur de recherche par mot-clé"
    title_print(titre)

    #Chargemement des documents
    with spinner_context():
        documents = load_data_exact()

    #Récupère les sections pour créer un radio boutons pour chaque + "Toutes"
    all_sections = get_available_sections(documents)
    sections_options = ["Toutes les sections"] + all_sections
    selected_section = radio_button("Choisissez une section", sections_options)

    #Récupère la requête 
    query = text_input()

    if query:
        #Preprocess de la requête
        query_cleaned = preprocess_query(query)
        #Vérifie les sections choisies
        selected_sections = None if selected_section == "Toutes les sections" else [selected_section]
        
        #Fais la recherche
        results = exact_search(documents, query_cleaned, selected_sections=selected_sections)
        
        #L'affichage des résultats
        display_exacte_results(results, query, selected_section)
