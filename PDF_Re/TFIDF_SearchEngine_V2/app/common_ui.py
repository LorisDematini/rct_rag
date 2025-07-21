"""
common_ui.py

Ce module contient les fonctions d'affichage pour l'interface utilisateur Streamlit 
du moteur de recherche, pour les recherches par similarité .

Fonctions :
- highlight_text(text, keywords) : Surligne les mots-clés dans un texte donné en utilisant des balises HTML <mark>.
- display_sparse_results(results, query) : Affiche les protocoles d'une recherche sparse sous forme de tableau avec surlignage des mots-clés.

"""

import os
import streamlit as st
import re
import json
from config.paths import SECTIONS_JSON_PATH, PDF_FOLDER, SECTIONS_FULL_JSON_PATH, SUMMARY_JSON_PATH
import matplotlib.pyplot as plt

import nltk
nltk.download('wordnet')
nltk.download('omw-1.4')
nltk.download('averaged_perceptron_tagger')

#Chargment unique du fichier summary.json 
with open(SECTIONS_JSON_PATH, "r", encoding="utf-8") as f:
    summary_data = json.load(f)

with open(SECTIONS_FULL_JSON_PATH, "r", encoding="utf-8") as f:
    summary_data_full = json.load(f)

with open(SUMMARY_JSON_PATH, "r", encoding="utf-8") as f:
    summary = json.load(f)

# #Fonction de surlignage
# def highlight_text(text, keywords):
#     for word in sorted(keywords, key=len, reverse=True):
#         pattern = re.compile(rf"(\b{re.escape(word)}\b)", flags=re.IGNORECASE)
#         text = pattern.sub(r"<mark>\1</mark>", text)
#     return text

def highlight_text_sparse(text, raw_query, cleaned_query):
    keywords = set()

    raw_terms = re.findall(r"\b\w+\b", raw_query.lower())
    cleaned_terms = re.findall(r"\b\w+\b", cleaned_query.lower())

    keywords.update(raw_terms)
    keywords.update(cleaned_terms)

    for word in sorted(keywords, key=len, reverse=True):
        pattern = re.compile(rf"(\b{re.escape(word)}\b)", flags=re.IGNORECASE)
        text = pattern.sub(r"<mark>\1</mark>", text)

    return text

def highlight_text_exact(text, query, mode="PHRASE"):
    text = str(text)
    original_text = text

    if mode == "PHRASE":
        phrase = query.strip().lower()
        if phrase.endswith("*"):
            prefix = re.escape(phrase[:-1])
            pattern = re.compile(rf"\b({prefix}\w*)\b", flags=re.IGNORECASE)
            return pattern.sub(r"<mark>\1</mark>", text)
        else:
            pattern = re.compile(rf"\b({re.escape(phrase)})\b", flags=re.IGNORECASE)
            return pattern.sub(r"<mark>\1</mark>", text)

    elif mode in ("AND", "OR"):
        terms = re.split(r"\s+(and|or)\s+", query.lower())
        keywords = [t.strip() for t in terms if t.lower() not in {"and", "or"} and t.strip()]

        for word in sorted(keywords, key=len, reverse=True):
            if word.endswith("*"):
                prefix = re.escape(word[:-1])
                pattern = re.compile(rf"\b({prefix}\w*)\b", flags=re.IGNORECASE)
            else:
                pattern = re.compile(rf"\b({re.escape(word)})\b", flags=re.IGNORECASE)
            text = pattern.sub(r"<mark>\1</mark>", text)

        return text

    return original_text




def clean_string(s):
    return s.lower().replace("-", " ").replace("_", " ").replace("/", " ").strip()

def find_pdf_file(study_id, folder=PDF_FOLDER):
    study_id_clean = clean_string(study_id)

    for filename in os.listdir(folder):
        if not filename.lower().endswith(".pdf"):
            continue

        fname_clean = clean_string(filename)

        # Match strict sur le début
        if fname_clean.startswith(study_id_clean):
            return os.path.join(folder, filename)

        # Match plus souple : inclusion dans le nom
        if study_id_clean in fname_clean:
            return os.path.join(folder, filename)
 
    return None

def display_sparse_results(results, query, query_cleaned, top_terms_by_study=None):
    if "validated_warning" not in st.session_state:
        st.session_state.validated_warning = False

    if not st.session_state.validated_warning:
        st.warning(f"requête traitée : `{query_cleaned}`")
        if st.button("✅ Continuer"):
            st.session_state.validated_warning = True
        else:
            st.stop()
    st.session_state.validated_warning = False

    keywords = query.split()
    total_results = len(results)
    total_studies = len(summary_data)

    st.subheader(f"{total_results} / {total_studies} protocoles trouvés")

    if not results:
        st.info("Aucun protocole pertinent trouvé.")
        return

   # SCORES
    study_ids = [res["study_id"] for res in results]
    scores = [res["score"] for res in results]

    fig, ax = plt.subplots(figsize=(10, 4))  #paysage
    bars = ax.bar(study_ids, scores, color='skyblue')
    ax.set_title("Score par protocole")
    ax.set_ylabel("Score de similarité")
    ax.set_xlabel("Identifiant du protocole")
    ax.set_ylim(0, max(scores) * 1.1)

    if len(study_ids) > 5:
        ax.set_xticklabels(study_ids, rotation=45, ha='right')

    st.pyplot(fig)

    for result in results:
        study_id = result["study_id"]
        score = result["score"]
        normalized_score = score

        color = "green" if normalized_score > 0.2 else "orange" if normalized_score > 0.1 else "red"
        st.markdown(f"### {study_id} — Score : <span style='color:{color}; font-weight:bold'>{normalized_score:.2f}</span>", unsafe_allow_html=True)

        if top_terms_by_study and study_id in top_terms_by_study:
            terms = top_terms_by_study[study_id]
            formatted_terms = ", ".join(f"**{term}** (`{score:.2f}`)" for term, score in terms)
            st.markdown(f"**Mots importants** : {formatted_terms}")

        with st.expander("Afficher les détails du protocole"):
            if study_id not in summary_data:
                st.warning("Aucune donnée trouvée dans le fichier summary.json pour ce protocole.")
                continue

            pdf_path = find_pdf_file(study_id)
            if pdf_path:
                with open(pdf_path, "rb") as file:
                    st.download_button(
                        label="📄 Télécharger le protocole (.pdf)",
                        data=file,
                        file_name=os.path.basename(pdf_path),
                        mime="application/pdf"
                    )
            else:
                st.info("Aucun fichier .pdf disponible pour ce protocole.")

            study_content = summary_data[study_id]
            if isinstance(study_content, dict):
                for section_title, section_paragraphs in study_content.items():
                    if not section_paragraphs:
                        continue
                    col1, col2 = st.columns([1, 4])
                    with col1:
                        st.markdown(f"**{section_title}**")
                    with col2:
                        if isinstance(section_paragraphs, list):
                            for paragraph in section_paragraphs:
                                if isinstance(paragraph, str):
                                    highlighted = highlight_text_sparse(paragraph, query, query_cleaned)
                                    st.markdown(highlighted, unsafe_allow_html=True)
                                else:
                                    st.markdown("Paragraphe non textuel.")
                        else:
                            st.markdown("Section invalide ou vide.")
            else:
                st.warning("Format inattendu pour ce protocole.")



def display_exacte_results(results, query, selected_section=None, engine=None):
    if engine is None:
        raise ValueError("L'objet engine est requis")
    parsed = engine.parse_query(query)
    mode = parsed["operator"]

    unique_study_ids = {res["study_id"] for res in results}
    total_results = len(unique_study_ids)
    total_studies = len(summary_data_full)

    if selected_section == "Toutes les sections":
        st.subheader(f"{total_results} / {total_studies} protocole(s) trouvé(s)")
    else :
        st.subheader(f"{total_results} section(s) trouvée(s)")

    if not results:
        st.info("Aucun protocole pertinent trouvé.")
        return

    #ne pas répéter plusieurs fois le même protocole
    display_all_sections = (selected_section is None) or (selected_section == "Toutes les sections")

    if display_all_sections:
        # Regrouper les protocoles par protocole pour éviter doublons
        results_by_study = {}
        for res in results:
            sid = res["study_id"]
            if sid not in results_by_study:
                results_by_study[sid] = res

        for study_id, res in results_by_study.items():
            st.markdown(f"### {study_id}")

            pdf_path = find_pdf_file(study_id)
            if pdf_path:
                with open(pdf_path, "rb") as file:
                    st.download_button(
                        label="📄 Télécharger le rapport (.pdf)",
                        data=file,
                        file_name=os.path.basename(pdf_path),
                        mime="application/pdf"
                    )
            else:
                st.info("Aucun fichier .pdf disponible pour ce protocole.")

            study_content = summary_data_full.get(study_id, {})

            if not isinstance(study_content, dict):
                st.warning("Format inattendu pour ce protocole.")
                continue

            with st.expander("Afficher toutes les sections"):
                for sec, section_paragraphs in study_content.items():
                    if not section_paragraphs:
                        continue
                    col1, col2 = st.columns([1, 4])
                    with col1:
                        st.markdown(f"**{sec}**")
                    with col2:
                        if isinstance(section_paragraphs, list):
                            for paragraph in section_paragraphs:
                                if isinstance(paragraph, str):
                                    highlighted = highlight_text_exact(paragraph, query, mode)
                                    st.markdown(highlighted, unsafe_allow_html=True)
                                else:
                                    st.markdown("Paragraphe non textuel.")
                        else:
                            st.markdown("Section invalide ou vide.")

    else:
        for result in results:
            study_id = result["study_id"]
            section_name = result.get("section_name", "UNKNOWN")

            st.markdown(f"### {study_id} — Section : {section_name}")

            pdf_path = find_pdf_file(study_id)
            if pdf_path:
                with open(pdf_path, "rb") as file:
                    st.download_button(
                        label="📄 Télécharger le rapport (.pdf)",
                        data=file,
                        file_name=os.path.basename(pdf_path),
                        mime="application/pdf"
                    )
            else:
                st.info("Aucun fichier .pdf disponible pour ce protocole.")

            study_content = summary_data_full.get(study_id, {})

            if not isinstance(study_content, dict):
                st.warning("Format inattendu pour ce protocole.")
                continue

            section_paragraphs = study_content.get(section_name, [])
            if not section_paragraphs:
                continue

            col1, col2 = st.columns([1, 4])
            with col1:
                st.markdown(f"**{section_name}**")
            with col2:
                if isinstance(section_paragraphs, list):
                    for paragraph in section_paragraphs:
                        if isinstance(paragraph, str):
                            highlighted = highlight_text_exact(paragraph, query, mode)
                            st.markdown(highlighted, unsafe_allow_html=True)
                        else:
                            st.markdown("Paragraphe non textuel.")
                else:
                    st.markdown("Section invalide ou vide.")


def display_liste(query=None):
    if query is None or query.strip() == "":
        st.subheader(f"Liste complète des {len(summary)} protocoles")

        filtered_summary = summary.items()
    else:
        query = query.strip().lower()
        # Filtrer les protocole contenant le mot dans le study_id
        filtered_summary = [
            (study_id, study_content)
            for study_id, study_content in summary.items()
            if query in study_id.lower()
        ]

        if not filtered_summary:
            st.warning("Aucun protocole trouvé avec ce nom.")
            return

    for study_id, study_content in filtered_summary:
        st.markdown(f"### {study_id}")

        # Bouton de téléchargement PDF
        pdf_path = find_pdf_file(study_id)
        if pdf_path:
            with open(pdf_path, "rb") as file:
                st.download_button(
                    label="📄 Télécharger le rapport (.pdf)",
                    data=file,
                    file_name=os.path.basename(pdf_path),
                    mime="application/pdf"
                )
        else:
            st.info("Aucun fichier .pdf disponible pour cette protocole.")

        # Expander pour afficher le contenu brut
        with st.expander("Afficher le contenu de protocole"):
            if isinstance(study_content, dict):
                for section_title, section_paragraphs in study_content.items():
                    if not section_paragraphs:
                        continue
                    col1, col2 = st.columns([1, 4])
                    with col1:
                        st.markdown(f"**{section_title}**")
                    with col2:
                        if isinstance(section_paragraphs, str):
                            st.markdown(section_paragraphs)
                        else:
                            st.markdown("Paragraphe non textuel.")
            else:
                st.warning("Format inattendu pour cette protocole.")


