import json
import matplotlib.pyplot as plt
import os
import plotly.graph_objects as go
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
import seaborn as sns

# Chemin
output_dir = "/home/loris/Stage/STAGE/Test/db_sortie_block/DOC/analysis/KMEANS/PCA"
os.makedirs(output_dir, exist_ok=True)

def load_data(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

# Section et études
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


def cluster_study_sections_with_pca(X_tfidf, labels, n_clusters=8):
    pca = PCA(n_components=3)
    X_pca = pca.fit_transform(X_tfidf.toarray())

    kmeans = KMeans(n_clusters=n_clusters, random_state=8)
    clusters = kmeans.fit_predict(X_pca)

    df = pd.DataFrame({
        'PCA1': X_pca[:, 0],
        'PCA2': X_pca[:, 1],
        'PCA3': X_pca[:, 2],
        'Cluster': clusters,
        'Section': [section for (_, section) in labels],
        'StudyID': [study_id for (study_id, _) in labels]
    })

    fig = go.Figure()

    palette = sns.color_palette("tab10", n_clusters).as_hex()

    for cluster in range(n_clusters):
        cluster_df = df[df['Cluster'] == cluster]
        fig.add_trace(go.Scatter3d(
            x=cluster_df['PCA1'],
            y=cluster_df['PCA2'],
            z=cluster_df['PCA3'],
            mode='markers+text',
            text=cluster_df['Section'],
            textposition='top center',
            marker=dict(
                size=6,
                color=palette[cluster],
                opacity=0.8
            ),
            name=f"Cluster {cluster}"
        ))

    fig.update_layout(
        title="Clustering des sections par étude via PCA 3D + KMeans (Interactif)",
        scene=dict(
            xaxis_title='PCA 1',
            yaxis_title='PCA 2',
            zaxis_title='PCA 3'
        ),
        margin=dict(l=0, r=0, b=0, t=40),
        legend=dict(x=0.02, y=0.98)
    )

    fig.show()
    print(f"Visualisation interactive sauvegardée dans : {output_dir}/Kmeans_etude_sections3D_interactif.html")

def main(json_file):
    studies = load_data(json_file)
    X_tfidf, labels = build_study_section_tfidf(studies)
    cluster_study_sections_with_pca(X_tfidf, labels)

    print(f"\nAnalyse KMeans-PCA 3D terminée. Résultat sauvegardé dans : {output_dir}")

if __name__ == "__main__":
    json_file = "/home/loris/Stage/STAGE/Test/db_sortie_block/DOC/grouped_titles_preprocessed.json"
    main(json_file)
