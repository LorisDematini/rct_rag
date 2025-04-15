from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import pairwise_distances
import numpy as np

# Données
texte1 = "test salut comment ça va"
documents = [texte1]
query = ["salut"]

print("Texte 1 :", texte1)
print("Requête :", query)

# TF-IDF
vectorizer = TfidfVectorizer(norm='l2')
X_docs = vectorizer.fit_transform(documents)
X_query = vectorizer.transform(query)

doc_vector = X_docs.toarray()[0]
query_vector = X_query.toarray()[0]

print("\nVecteur du texte :", doc_vector)
print("Vecteur de la requête :", query_vector)

# === DISTANCE COSINUS ===

#Produit scalaire
dot_product = np.dot(doc_vector, query_vector)
print(f"\nProduit scalaire (dot product) :")
print(f"  dot_product = {dot_product:.4f}")

#Norme du vecteur du texte
norm_doc = np.linalg.norm(doc_vector)
print(f"\nNorme du vecteur du texte :")
print(f"  norm_doc = ||doc_vector|| = √({np.sum(doc_vector ** 2)}) = {norm_doc:.4f}")

#Norme du vecteur de la requête
norm_query = np.linalg.norm(query_vector)
print(f"\nNorme du vecteur de la requête :")
print(f"  norm_query = ||query_vector|| = √({np.sum(query_vector ** 2)}) = {norm_query:.4f}")

# Similarité cosinus
cosine_manual = 1 - dot_product / (norm_doc * norm_query)
print(f"\nCalcul de la distance cosinus :")
print(f"  cosine_manual = 1 - (dot_product / (norm_doc * norm_query)) = 1 - ({dot_product:.4f} / ({norm_doc:.4f} * {norm_query:.4f})) = {cosine_manual:.4f}")

#Cosinus manuelle
print("\n Distance cosinus manuelle :", cosine_manual)

#Sklearn
cosine_sklearn = pairwise_distances([doc_vector], [query_vector], metric='cosine')[0][0]
print("\n Distance cosinus (sklearn) :", cosine_sklearn)
