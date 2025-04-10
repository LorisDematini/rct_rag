import json
import matplotlib.pyplot as plt
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
import seaborn as sns

output_dir = "/home/loris/Stage/STAGE/Test/db_sortie_block/DOC/analysis/KMEANS/PCA"
os.makedirs(output_dir, exist_ok=True)

def load_data(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

def build_intersection_tfidf_analysis(studies, sections=['SUMMARY','SCIENTIFIC JUSTIFICATION','OBJECTIVES','METHODOLOGY','PROCEDURE','ELIGIBILITY','DATA MANAGEMENT','STATISTICAL']):
    section_texts = []
    valid_sections = []

    for section in sections:
        all_texts = []
        for study in studies.values():
            if section in study and isinstance(study[section], str):
                all_texts.append(study[section])

        if all_texts:
            full_text = " ".join(all_texts)
            section_texts.append(full_text)
            valid_sections.append(section)
        else:
            print(f"Section vide ou manquante : {section}")

    vectorizer = TfidfVectorizer(
        max_df=0.9,
        min_df=2,
        lowercase=True
    )

    X_mat = vectorizer.fit_transform(section_texts)
    return X_mat, valid_sections

def cluster_sections_with_pca(X_tfidf, valid_sections, n_clusters=8):

    pca = PCA(n_components=2)
    X_pca = pca.fit_transform(X_tfidf.toarray())

    kmeans = KMeans(n_clusters=n_clusters, random_state=8)
    clusters = kmeans.fit_predict(X_pca)

    plt.figure(figsize=(10, 6))
    palette = sns.color_palette("hsv", n_clusters)
    for i, section in enumerate(valid_sections):
        plt.scatter(X_pca[i, 0], X_pca[i, 1], c=[palette[clusters[i]]], label=section, s=100)

    for i, section in enumerate(valid_sections):
        plt.text(X_pca[i, 0]+0.01, X_pca[i, 1]+0.01, section, fontsize=9)

    plt.title("Clustering des sections via PCA + KMeans")
    plt.xlabel("PCA 1")
    plt.ylabel("PCA 2")
    plt.grid(True)
    plt.tight_layout()
    plt.legend()
    plt.savefig(f"{output_dir}/Kmeans_sections.png")
    plt.close()

def main(json_file):

    studies = load_data(json_file)
    X_tfidf, valid_sections = build_intersection_tfidf_analysis(studies)
    cluster_sections_with_pca(X_tfidf, valid_sections)

    print(f"\n Analyse KMeans-PCA terminée. Résultat unique dans : {output_dir}")

if __name__ == "__main__":
    json_file = "/home/loris/Stage/STAGE/Test/db_sortie_block/DOC/grouped_titles_preprocessed.json"
    main(json_file)
