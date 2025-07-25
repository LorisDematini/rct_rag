"""
display_sparse.py

Module d'affichage des résultats de recherche TF-IDF dans l'interface Streamlit.

Fonctions principales :
- display_sparse_results(results, query, query_cleaned, top_terms_by_study) :
    Affiche les résultats de recherche dense en listant les protocoles trouvés,
    leurs scores, mots-clés les plus importants, et un lien de téléchargement vers le PDF.

- display_scores_chart(results) :
    Génère un graphique matplotlib affichant le score de similarité pour chaque protocole.

- display_study_sections(sections, query, cleaned_query) :
    Affiche les sections et paragraphes d’un protocole avec mise en évidence des termes (highlight).

Fonctionnalités :
- Affichage conditionnel d’un avertissement sur la requête nettoyée (`query_cleaned`).
- Coloriage du score en fonction de son importance.
- Téléchargement du fichier PDF si disponible.
- Highlight HTML des mots de la requête dans le texte (via `highlight_text_sparse` ou `highlight_text_exact`).
- Graphique des scores pour visualiser la pertinence relative des protocoles.
"""

import os
import streamlit as st
import matplotlib.pyplot as plt

from display.highlight import highlight_text_sparse, highlight_text_exact
from display.display_utils import find_pdf_file, get_summary_data, get_summary_data_full, get_summary_list

summary_data = get_summary_data()
summary_data_full = get_summary_data_full()
summary = get_summary_list()

#Affichage du graphique en fonction des résultats
def display_scores_chart(results):
    study_ids = [r["study_id"] for r in results]
    scores = [r["score"] for r in results]
    fig, ax = plt.subplots(figsize=(10, 4))
    bars = ax.bar(study_ids, scores, color='skyblue')
    ax.set(title="Score par protocole", xlabel="Protocole", ylabel="Score", ylim=(0, max(scores)*1.1))
    #Tourne les noms d'étude si ils sont trop nombreux 
    if len(study_ids) > 5:
        ax.set_xticks(range(len(study_ids)))
        ax.set_xticklabels(study_ids, rotation=45, ha='right')
    st.pyplot(fig)

#Affichage du contenu des sections 
def display_study_sections(sections, query, cleaned_query):
    if not isinstance(sections, dict):
        st.warning("Format invalide pour ce protocole.")
        return

    for title, paragraphs in sections.items():
        if not paragraphs:
            continue
        # Une colonne pour le nom de la section et 4 pour le contenu du texte
        col1, col2 = st.columns([1, 4])
        with col1:
            st.markdown(f"**{title}**")
        with col2:
            for p in paragraphs if isinstance(paragraphs, list) else [paragraphs]:
                if not isinstance(p, str):
                    st.markdown("Paragraphe non textuel.")
                    continue
                #on appelle ici la fonction highlight
                st.markdown(highlight_text_sparse(p, query, cleaned_query), unsafe_allow_html=True)

def display_sparse_results(results, query, query_cleaned, top_terms_by_study):
    #Affiche un avertissement à cliquer pour poursuivre la recherche après écriture de la requête
    if "validated_warning" not in st.session_state:
        st.session_state.validated_warning = False

    if not st.session_state.validated_warning:
        st.warning(f"requête traitée : `{query_cleaned}`")
        if not st.button("✅ Continuer"):
            st.stop()
    st.session_state.validated_warning = False

    #Nombre de résultats
    st.subheader(f"{len(results)} / {len(summary_data)} protocoles trouvés")
    if not results:
        st.info("Aucun protocole pertinent trouvé.")
        return

    #Graphiques des résultats
    display_scores_chart(results)

    for res in results:
        study_id = res["study_id"]
        score = res["score"]
        #Code couleurs des scores
        color = "green" if score > 0.2 else "orange" if score > 0.1 else "red"
        st.markdown(f"### {study_id} — Score : <span style='color:{color}'><b>{score:.2f}</b></span>", unsafe_allow_html=True)

        if top_terms_by_study and study_id in top_terms_by_study:
            top_terms = top_terms_by_study[study_id]
            terms = ", ".join(f"**{term}** (`{s:.2f}`)" for term, s in top_terms)
            st.markdown(f"**Mots importants :** {terms}")
            
            #Affichage des téléchargements de PDF
            pdf_path = find_pdf_file(study_id)
            if pdf_path:
                with open(pdf_path, "rb") as file:
                    st.download_button(
                        label="📄 Télécharger le rapport (.pdf)",
                        data=file,
                        file_name=pdf_path.split(os.sep)[-1],
                        mime="application/pdf"
                    )
            else:
                st.info("Aucun fichier .pdf disponible pour ce protocole.")

        #Affiche les sections du texte de la base sans preprocess
        with st.expander("Afficher les détails"):
            display_study_sections(summary_data.get(study_id), query, query_cleaned)
