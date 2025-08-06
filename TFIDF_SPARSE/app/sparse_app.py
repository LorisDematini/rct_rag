'''
sparse_app.py

Ce module exécute l'application Streamlit pour la recherche par similarité (basée sur TF-IDF).

Fonction principale : `run_sparse_app()`

Étapes principales :
1. Affiche le titre "Moteur de recherche par similarité".
2. Charge les documents prétraités à l’aide de `load_data_sparse()`.
3. Construit l’index TF-IDF via `build_sparse_index()` (retourne le vectoriser, la matrice sparse, les study_ids et les documents).
4. Récupère la requête utilisateur, puis la prétraite avec `preprocess_query()`.
5. Effectue la recherche par similarité cosinus avec `search_sparse()`.
6. Récupère les termes les plus importants par étude (`get_top_terms()`).
7. Affiche les résultats de recherche et de top termes avec `display_sparse_results()`.

Ce moteur permet une recherche par similarité, en utilisant la pondération TF-IDF pour trouver les sections les plus proches de la requête en termes de contenu.
'''


from core.data_loader import load_data_sparse, load_sparse_index, load_top_terms
from core.sparse_search import search_sparse
from preprocess.processed_sparse import preprocess_query
from display.display_sparse import display_sparse_results
from display.display_utils import spinner_context, title_print, text_input

#Fonction principale
def run_sparse_app():
    titre = "Moteur de recherche par similarité"
    title_print(titre)

    with spinner_context():
        print("[INFO] Chargement des données sparse...")
        #Chargement des documents et création de la matrice, du vectoriser et la liste des études
        documents = load_data_sparse()
        vectorizer, sparse_matrix, study_ids = load_sparse_index()
        #Récupération des top termes de chaque études
        top_terms_by_study = load_top_terms()

    query = text_input()

    if query:
        query_cleaned = preprocess_query(query)
        print(f"Requête prétraitée : {query_cleaned}")

        #Effectue la recherche avec une similarité cosinus et la requête
        results = search_sparse(query_cleaned, vectorizer, sparse_matrix, study_ids, documents)

        #Affichage de tous les résultats
        display_sparse_results(results, query, query_cleaned, top_terms_by_study)
