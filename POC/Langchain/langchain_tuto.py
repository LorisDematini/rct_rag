import streamlit as st
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.schema import Document
import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")
st.title("🔍 Moteur de recherche sémantique — Démo + Embeddings visibles")

# --- Données simples ---
st.subheader("🗂 Jeu de données d'exemple")
exemples = {
    "Doc1": "Le chat dort sur le canapé.",
    "Doc2": "Le chien joue dans le jardin.",
    "Doc3": "Il fait beau aujourd'hui.",
    "Doc4": "Les chats aiment dormir toute la journée.",
    "Doc5": "La météo est agréable au printemps."
}
for titre, contenu in exemples.items():
    st.markdown(f"**{titre}** : {contenu}")

# --- Embedding
documents = [Document(page_content=texte, metadata={"title": titre}) for titre, texte in exemples.items()]
st.info("📥 Génération des vecteurs d'embedding...")
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2", model_kwargs={"device": "cpu"})

# --- Génération des vecteurs ---
doc_vectors = embeddings.embed_documents([doc.page_content for doc in documents])
titles = [doc.metadata["title"] for doc in documents]

# --- Affichage des vecteurs ---
with st.expander("🔢 Afficher les vecteurs d'embedding (documents)"):
    df_vec = pd.DataFrame(doc_vectors, index=titles)
    st.dataframe(df_vec.style.format(precision=3), use_container_width=True)

# --- FAISS Index ---
vectorstore = FAISS.from_documents(documents, embeddings)
st.success("✅ Indexation terminée")

# --- Requête utilisateur ---
query = st.text_input("🔍 Entrez votre requête", "chat qui dort")
if query:
    results = vectorstore.similarity_search_with_score(query, k=3)
    query_vector = embeddings.embed_query(query)

    st.subheader("📊 Résultats de la recherche")
    for doc, score in results:
        similarity = 1 / (1 + score)
        st.markdown(f"**{doc.metadata['title']}** — Similarité : `{similarity:.4f}`")
        with st.expander("Afficher le contenu du document"):
            st.write(doc.page_content)

    # --- Similarités manuelles ---
    cos_sim = cosine_similarity([query_vector], doc_vectors).flatten()
    sim_df = pd.DataFrame({"Titre": titles, "Similarité Cosine": cos_sim})
    st.subheader("📈 Similarités Cosine entre la requête et les documents")
    st.dataframe(sim_df.sort_values("Similarité Cosine", ascending=False).style.format(precision=4), use_container_width=True)

    # --- Visualisation 2D (PCA) ---
    st.subheader("🧭 Visualisation des embeddings (PCA)")
    pca = PCA(n_components=2)
    reduced = pca.fit_transform(np.vstack([doc_vectors, query_vector]))

    fig, ax = plt.subplots()
    ax.scatter(reduced[:-1, 0], reduced[:-1, 1], label="Documents", color="skyblue")
    ax.scatter(reduced[-1, 0], reduced[-1, 1], label="Requête", color="orange", marker="X", s=100)
    for i, title in enumerate(titles):
        ax.text(reduced[i, 0] + 0.02, reduced[i, 1], title, fontsize=9)
    ax.legend()
    ax.set_title("Projection PCA des vecteurs")
    st.pyplot(fig)
