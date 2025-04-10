import json
import matplotlib.pyplot as plt
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
import seaborn as sns

#Chemin
output_dir = "/home/loris/Stage/STAGE/Test/db_sortie_block/DOC/analysis/KMEANS/PCA"
os.makedirs(output_dir, exist_ok=True)

def load_data(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

#Chaque section d'une étude
def build_study_section_tfidf(studies, sections=['SUMMARY','SCIENTIFIC JUSTIFICATION','OBJECTIVES','METHODOLOGY','ELIGIBILITY','STATISTICAL']):
    texts = []
    labels = []

    for study_id, study in studies.items():
        for section in sections:
            if section in study and isinstance(study[section], str) and study[section].strip():
                texts.append(study[section])
                labels.append((study_id, section))

    vectorizer = TfidfVectorizer(
        stop_words='english',
        max_df=0.9,
        min_df=2,
        lowercase=True
    )
    X_mat = vectorizer.fit_transform(texts)
    return X_mat, labels

#Traitement des sections des études
def cluster_study_sections_with_pca(X_tfidf, labels, n_clusters=6):

    pca = PCA(n_components=2)
    X_pca = pca.fit_transform(X_tfidf.toarray())

    kmeans = KMeans(n_clusters=n_clusters, random_state=8)
    clusters = kmeans.fit_predict(X_pca)

    plt.figure(figsize=(12, 8))
    palette = sns.color_palette("tab10", n_clusters)

    for i, (study_id, section) in enumerate(labels):
        plt.scatter(X_pca[i, 0], X_pca[i, 1], c=[palette[clusters[i]]], label=f"{section}", s=50)
        plt.text(X_pca[i, 0]+0.01, X_pca[i, 1]+0.01, section, fontsize=7)

    plt.title("Clustering des sections par étude via PCA + KMeans")
    plt.xlabel("PCA 1")
    plt.ylabel("PCA 2")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(f"{output_dir}/Kmeans_etude_section_zoom.png")
    plt.close()

#Main
def main(json_file):

    studies = load_data(json_file)
    X_tfidf, labels = build_study_section_tfidf(studies)
    cluster_study_sections_with_pca(X_tfidf, labels)

    print(f"\nAnalyse KMeans-PCA terminée. Résultat unique dans : {output_dir}")

if __name__ == "__main__":
    json_file = "/home/loris/Stage/STAGE/Test/db_sortie_block/DOC/grouped_titles_preprocessed.json"
    main(json_file)
