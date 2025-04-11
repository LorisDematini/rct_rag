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
def build_study_section_tfidf(studies, sections=['SUMMARY','SCIENTIFIC JUSTIFICATION','OBJECTIVES','METHODOLOGY','PROCEDURE','DATA_MANAGEMENT','ELIGIBILITY','STATISTICAL']):
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

    top_terms_dict = show_top_terms_per_cluster(X_tfidf, clusters=clusters, vectorizer=vectorizer)

    plt.figure(figsize=(12, 8))
    palette = sns.color_palette("tab10", n_clusters)

    for cluster_id in range(n_clusters):
        cluster_points = X_tsne[clusters == cluster_id]
        plt.scatter(cluster_points[:, 0], cluster_points[:, 1], 
                    c=[palette[cluster_id]], 
                    label=f"Cluster {cluster_id}", 
                    s=50)
        centroid_x, centroid_y = cluster_points.mean(axis=0)
        terms = ", ".join(top_terms_dict[cluster_id][:5])
        plt.text(centroid_x, centroid_y, f"Cluster {cluster_id}\n{terms}",
                 fontsize=9, weight='bold', color=palette[cluster_id])

    # Affichage des noms de section
    for i, (study_id, section) in enumerate(labels):
        plt.text(X_tsne[i, 0] + 0.01, X_tsne[i, 1] + 0.01, section, fontsize=7)

    plt.title("Clustering des sections par étude via t-SNE + KMeans")
    plt.xlabel("t-SNE 1")
    plt.ylabel("t-SNE 2")
    plt.legend(title="Clusters", loc="best")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(f"{output_dir}/Kmeans_etude_sections.png")
    plt.close()

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





def main(json_file):
    studies = load_data(json_file)
    X_tfidf, labels, texts, vectorizer = build_study_section_tfidf(studies)
    cluster_study_sections_with_tsne(X_tfidf, labels, texts, vectorizer)

    print(f"\nAnalyse KMeans-tSNE terminée. Résultat image + CSV dans : {output_dir}")

if __name__ == "__main__":
    json_file = "/home/loris/Stage/STAGE/Test/db_sortie_block/DOC/Extract/grouped_titles_preprocessed.json"
    main(json_file)
