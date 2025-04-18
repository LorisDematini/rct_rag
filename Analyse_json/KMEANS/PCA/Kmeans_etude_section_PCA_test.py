import json
import matplotlib.pyplot as plt
import os
import seaborn as sns
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
import numpy as np

# Chemin de sortie pour les résultats
output_dir = "/home/loris/Stage/STAGE/Test/db_sortie_block/DOC/analysis/KMEANS/PCA"
os.makedirs(output_dir, exist_ok=True)

# Charger les données à partir du fichier JSON
def load_data(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

# Fonction pour générer la matrice TF-IDF des sections des études
def build_study_section_tfidf(studies, sections=['SUMMARY','SCIENTIFIC JUSTIFICATION','OBJECTIVES','METHODOLOGY','PROCEDURE','ELIGIBILITY','DATA MANAGEMENT','STATISTICAL']):
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
    return X_mat, labels

# Fonction pour effectuer PCA, calculer la variance expliquée et le clustering KMeans
def cluster_study_sections_with_pca(X_tfidf, labels, n_clusters=8, n_components=2):
    # Appliquer PCA
    pca = PCA(n_components=n_components)
    X_pca = pca.fit_transform(X_tfidf.toarray())

    # Calcul de la variance expliquée
    explained_variance = pca.explained_variance_ratio_
    print(f"\n Variance expliquée par les composantes PCA :")
    for i, var in enumerate(explained_variance, 1):
        print(f"  - Composante {i}: {var:.2%}")

    # Si plus de 2 composantes, on peut afficher la variance cumulée
    if n_components > 2:
        plt.figure()
        plt.plot(range(1, n_components + 1), np.cumsum(explained_variance), marker='o')
        plt.title("Variance expliquée cumulée")
        plt.xlabel("Nombre de composantes")
        plt.ylabel("Variance expliquée cumulée")
        plt.grid(True)
        plt.savefig(f"{output_dir}/variance_expliquee_pca.png")
        plt.close()

    # Clustering avec KMeans
    kmeans = KMeans(n_clusters=n_clusters, random_state=8)
    clusters = kmeans.fit_predict(X_pca)

    # Visualisation du clustering avec PCA (2D ou 3D)
    plt.figure(figsize=(12, 8))
    palette = sns.color_palette("tab10", n_clusters)

    for i, (study_id, section) in enumerate(labels):
        plt.scatter(X_pca[i, 0], X_pca[i, 1], c=[palette[clusters[i]]], s=50)
        plt.text(X_pca[i, 0] + 0.01, X_pca[i, 1] + 0.01, section, fontsize=7)

    plt.title(f"Clustering des sections par étude via PCA + KMeans (PCA {n_components})")
    plt.xlabel(f"PCA 1 ({explained_variance[0]:.1%} var.)")
    plt.ylabel(f"PCA 2 ({explained_variance[1]:.1%} var.)")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(f"{output_dir}/Kmeans_etude_sections.png")
    plt.close()

def main(json_file):
    studies = load_data(json_file)
    X_tfidf, labels = build_study_section_tfidf(studies)
    cluster_study_sections_with_pca(X_tfidf, labels)

    print(f"\nAnalyse KMeans-PCA terminée. Résultat unique dans : {output_dir}")

if __name__ == "__main__":
    json_file = "/home/loris/Stage/STAGE/Test/db_sortie_block/DOC/Extract/grouped_titles_preprocessed.json"
    main(json_file)