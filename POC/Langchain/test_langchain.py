import streamlit as st
import json
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.schema import Document
import pandas as pd

# --- Titre ---
st.title("🔎 Moteur de recherche sémantique avec LangChain + HuggingFace (v0.2+)")

# --- Upload JSON ---
json_file = st.file_uploader("Uploader un fichier JSON contenant des résumés", type="json")

if json_file:
    data = json.load(json_file)
    docs = [{"title": key, "text": value["Summary"]} for key, value in data.items() if "Summary" in value]

    if not docs:
        st.warning("Aucun champ 'Summary' trouvé dans le fichier JSON.")
    else:
        # --- Construction des documents LangChain ---
        langchain_docs = [Document(page_content=doc["text"], metadata={"title": doc["title"]}) for doc in docs]

        # --- Embeddings ---
        #all-MiniLM-L6-v2 (rapide, efficace)
        # all-mpnet-base-v2 (plus précis)
        # multi-qa-MiniLM-L6-cos-v1 (optimisé pour la QA et recherche)
        
        st.info("Chargement du modèle d'embedding...")
        embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

        # --- FAISS Index ---
        st.info("Indexation FAISS...")
        vectorstore = FAISS.from_documents(langchain_docs, embeddings)

        # --- Interface utilisateur ---
        st.success("Indexation terminée. Vous pouvez lancer une recherche.")
        query = st.text_input("🔍 Entrez votre requête", "Votre requête ici")

        if query:
            results = vectorstore.similarity_search_with_score(query, k=5)

            st.subheader("📊 Résultats de la recherche")
            for doc, score in results:
                similarity = 1 / (1 + score)
                st.markdown(f"**{doc.metadata['title']}** —  Similarité : `{similarity:.4f}`")
                with st.expander("Afficher le résumé"):
                    st.write(doc.page_content)