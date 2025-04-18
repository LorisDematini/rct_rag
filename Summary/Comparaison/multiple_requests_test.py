from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import pairwise_distances
import numpy as np

# Données
texte1 = "test salut comment ça va"
texte2 = "test lung medical analyse cancer"
documents = [texte1, texte2]
query = ["test salut"]

print("Texte 1 :", texte1)
print("Texte 2 :", texte2)
print("Requête :", query)

# TF-IDF
vectorizer = TfidfVectorizer(norm='l2')
X_docs = vectorizer.fit_transform(documents)
X_query = vectorizer.transform(query)

# Conversion en array
docs_array = X_docs.toarray()
query_array = X_query.toarray()[0]

# Affichage des résultats
print("Documents :",docs_array)
print("\nVecteur de la requête :", query_array)

# Calcul de la distance cosinus manuelle pour chaque document
print("\n--- Calcul manuel des distances cosinus ---")
for i, doc_vec in enumerate(docs_array):
    dot_product = np.dot(doc_vec, query_array)
    norm_doc = np.linalg.norm(doc_vec)
    norm_query = np.linalg.norm(query_array)
    cosine_distance = 1 - dot_product / (norm_doc * norm_query)

    print(f"\nDocument {i+1}:")
    print(f"  dot_product = {dot_product:.4f}")
    print(f"  norm_doc = {norm_doc:.4f}")
    print(f"  norm_query = {norm_query:.4f}")
    print(f"  cosine_distance = {cosine_distance:.4f}")

# Avec sklearn
cosine_distances_sklearn = pairwise_distances(X_docs, X_query, metric='cosine')

print("\n--- Similarité cosinus (avec sklearn) ---")
for i, dist in enumerate(cosine_distances_sklearn):
    print(f"Document {i+1} vs Requête : {1-dist[0]:.4f}")
