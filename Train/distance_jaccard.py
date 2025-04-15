from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import jaccard_score
import numpy as np

# Données
texte1 = "test salut comment ça va salut"
documents = [texte1]
query = ["salut"]

print("Texte 1 :", texte1)
print("Requête :", query)

# Vectorisation binaire (présence/absence)
vectorizer = CountVectorizer(binary=True)
X_docs = vectorizer.fit_transform(documents)
X_query = vectorizer.transform(query)

doc_vector = X_docs.toarray()[0]
query_vector = X_query.toarray()[0]

print("\nVecteur binaire du texte :", doc_vector)
print("Vecteur binaire de la requête :", query_vector)

# Intersection
intersection = np.logical_and(doc_vector, query_vector).sum()
# Union
union = np.logical_or(doc_vector, query_vector).sum()
# Jaccard manuelle
jaccard_manual = intersection / union if union != 0 else 0

print(f"\nIntersection : {intersection}")
print(f"Union : {union}")
print(f"\nScore de Jaccard (manuel) = intersection / union = {jaccard_manual:.4f}")

# Avec sklearn
jaccard_lib = jaccard_score(doc_vector, query_vector)
print("Score de Jaccard (sklearn) :", jaccard_lib)
