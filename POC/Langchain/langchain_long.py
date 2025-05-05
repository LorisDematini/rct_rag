import streamlit as st
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.schema import Document
import pandas as pd
import json

# --- Titre ---
st.title("Moteur de recherche sémantique avec LangChain + HuggingFace")

#donnes json lu du fichier
with open("/home/loris/Stage/STAGE/Test/db_sortie_block/DOC/Summary/summary_tables_gather.json", "r") as file:
    data = json.load(file)
    

docs = [{"title": key, "text": value["Summary"]} for key, value in data.items() if "Summary" in value]

# --- Construction des documents LangChain ---
langchain_docs = [Document(page_content=doc["text"], metadata={"title": doc["title"]}) for doc in docs]

# --- Embeddings ---
st.info("Chargement du modèle d'embedding...")
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")

# --- FAISS Index ---
st.info("Indexation FAISS...")
vectorstore = FAISS.from_documents(langchain_docs, embeddings, normalize_L2=True)

# --- Interface utilisateur ---
st.success("Indexation terminée. Vous pouvez lancer une recherche.")
query = st.text_input(" Entrez votre requête", "Votre requête ici")

if query:
    results = vectorstore.similarity_search_with_score(query, k=5)

    st.subheader(" Résultats de la recherche")
    for doc, score in results:
        similarity = 1 / (1 + score)
        st.markdown(f"**{doc.metadata['title']}** —  Similarité : `{similarity:.4f}`")
        with st.expander("Afficher le résumé"):
            st.write(doc.page_content)
