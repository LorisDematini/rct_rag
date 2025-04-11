import json
import matplotlib.pyplot as plt
import os
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import seaborn as sns
from sklearn.manifold import TSNE

# Chemin
output_dir = "/home/loris/Stage/STAGE/Test/db_sortie_block/DOC/analysis/KMEANS/T-SNE"
os.makedirs(output_dir, exist_ok=True)

def load_data(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

# Section et études
def build_study_section_tfidf(studies, sections=['SUMMARY','SCIENTIFIC JUSTIFICATION','OBJECTIVES','METHODOLOGY','PROCEDURE','DATA MANAGEMENT','ELIGIBILITY','STATISTICAL']):
    texts = []
    labels = []

    for study_id, study in studies.items():
        for section in sections:
            if section in study and isinstance(study[section], str) and study[section].strip():
                texts.append(study[section])
                labels.append((study_id, section))

    vectorizer = TfidfVectorizer(
        max_df=0.9,
        min_df=2,
        lowercase=True
    )
    X_mat = vectorizer.fit_transform(texts)
    return X_mat, labels, texts, vectorizer

def cluster_study_sections_with_tsne(X_tfidf, labels, texts, vectorizer, n_clusters=4):
    n_samples = X_tfidf.shape[0]
    perplexity = min(30, max(5, n_samples // 3))
    tsne = TSNE(n_components=2, perplexity=perplexity, random_state=8)
    X_tsne = tsne.fit_transform(X_tfidf.toarray())

    kmeans = KMeans(n_clusters=n_clusters, random_state=8)
    clusters = kmeans.fit_predict(X_tsne)

    #Récupération des top termes par cluster
    top_terms_dict = show_top_terms_per_cluster(X_tfidf, clusters=clusters, vectorizer=vectorizer)

        # Visualisation avec top terms sur les centroïdes
    plt.figure(figsize=(12, 8))
    palette = sns.color_palette("tab10", n_clusters)

    for i, (study_id, section) in enumerate(labels):
        plt.scatter(X_tsne[i, 0], X_tsne[i, 1], c=[palette[clusters[i]]], s=50)
        plt.text(X_tsne[i, 0] + 0.01, X_tsne[i, 1] + 0.01, section, fontsize=7)

    #Ajouter les top termes sur le centroïde de chaque cluster
    for cluster_id in range(n_clusters):
        cluster_points = X_tsne[clusters == cluster_id]
        centroid_x, centroid_y = cluster_points.mean(axis=0)
        terms = ", ".join(top_terms_dict[cluster_id][:5])
        plt.text(centroid_x, centroid_y, f"Cluster {cluster_id}\n{terms}",
                 fontsize=9, weight='bold', color=palette[cluster_id])

    plt.title("Clustering des sections par étude via t-SNE + KMeans")
    plt.xlabel("t-SNE 1")
    plt.ylabel("t-SNE 2")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(f"{output_dir}/Kmeans_etude_sections.png")
    plt.close()

    #Sauvegarde CSV enrichi
    df = pd.DataFrame({
        "study_id": [s for s, sec in labels],
        "section": [sec for s, sec in labels],
        "cluster": clusters,
        "x_tsne": X_tsne[:, 0],
        "y_tsne": X_tsne[:, 1],
        "text": texts,
        "top_terms": [", ".join(top_terms_dict[c]) for c in clusters]
    })

    csv_path = os.path.join(output_dir, "kmeans_etude_section.csv")
    df.to_csv(csv_path, index=False)
    print(f"\n✅ CSV sauvegardé avec top_terms : {csv_path}")

    #Textes représentatifs pour chaque cluster
    show_representative_texts(X_tfidf, texts, clusters)


def show_top_terms_per_cluster(X_tfidf, clusters, vectorizer, n_terms=10):
    df = pd.DataFrame(X_tfidf.toarray())
    df["cluster"] = clusters

    top_terms = {}
    for k in sorted(df["cluster"].unique()):
        mean_vec = df[df["cluster"] == k].drop(columns="cluster").mean()
        top_idx = mean_vec.argsort()[::-1][:n_terms]
        terms = [vectorizer.get_feature_names_out()[i] for i in top_idx]
        top_terms[k] = terms
        print(f"\n Cluster {k} - top terms:")
        print(", ".join(terms))
    
    return top_terms


def show_representative_texts(X_tfidf, texts, clusters, n=3):
    df = pd.DataFrame(X_tfidf.toarray())
    df["cluster"] = clusters
    df["text"] = texts

    for cluster_id in sorted(df["cluster"].unique()):
        print(f"\n Cluster {cluster_id} - exemples de textes représentatifs :")
        cluster_df = df[df["cluster"] == cluster_id]
        centroid = cluster_df.drop(columns=["cluster", "text"]).mean().values
        distances = cluster_df.drop(columns=["cluster", "text"]).apply(lambda row: np.linalg.norm(row - centroid), axis=1)
        top_texts = cluster_df.loc[distances.nsmallest(n).index]["text"]
        for i, t in enumerate(top_texts):
            print(f"  {i+1}. {t[:200].replace('\n', ' ')}...")

# Méthode du coude
def elbow_method(X, max_k=10):
    inertias = []
    K_range = range(2, max_k + 1)

    for k in K_range:
        kmeans = KMeans(n_clusters=k, random_state=8)
        kmeans.fit(X)
        inertias.append(kmeans.inertia_)

    plt.figure(figsize=(8, 5))
    plt.plot(K_range, inertias, marker='o')
    plt.xlabel('Nombre de clusters')
    plt.ylabel('Inertie (Within-Cluster SSE)')
    plt.title('Méthode du coude pour déterminer le nombre de clusters optimal')
    plt.grid(True)
    plt.xticks(K_range)
    plt.tight_layout()
    elbow_path = os.path.join(output_dir, "elbow_method.png")
    plt.savefig(elbow_path)
    plt.close()
    print(f"📉 Graphe de la méthode du coude sauvegardé : {elbow_path}")




def main(json_file):
    studies = load_data(json_file)
    X_tfidf, labels, texts, vectorizer = build_study_section_tfidf(studies)

    # 🔍 Étape préliminaire : méthode du coude
    elbow_method(X_tfidf, max_k=12)

    # 🔁 Tu peux soit utiliser le résultat visuel pour décider de `n_clusters`
    # soit automatiser une heuristique ensuite
    cluster_study_sections_with_tsne(X_tfidf, labels, texts, vectorizer, n_clusters=8)

    print(f"\n✅ Analyse KMeans-tSNE terminée. Résultat image + CSV dans : {output_dir}")


if __name__ == "__main__":
    json_file = "/home/loris/Stage/STAGE/Test/db_sortie_block/DOC/Extract/grouped_titles_preprocessed.json"
    main(json_file)
