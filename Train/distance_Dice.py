from sklearn.feature_extraction.text import CountVectorizer
import numpy as np

# Données
texte1 = "test salut comment ça va salut"
texte2 = "test medical analyse cancer"
documents = [texte1, texte2]
query = ["salut test lung"]

print("Texte 1 :", texte1)
print("Texte 2 :", texte2)
print("Requête :", query)

# Vectorisation binaire (présence/absence)
vectorizer = CountVectorizer(binary=True)
X_docs = vectorizer.fit_transform(documents)
X_query = vectorizer.transform(query)

doc_vector = X_docs.toarray()[0]
query_vector = X_query.toarray()[0]

print("\nVecteur binaire du texte :", doc_vector)
print("Vecteur binaire de la requête :", query_vector)

# Intersection (mots présents dans les deux)
intersection = np.logical_and(doc_vector, query_vector).sum()
# Taille des vecteurs (nombre de mots présents)
size_doc = doc_vector.sum()
size_query = query_vector.sum()

# Dice coefficient manuel
dice_manual = (2 * intersection) / (size_doc + size_query) if (size_doc + size_query) != 0 else 0

print(f"\nIntersection : {intersection}")
print(f"Taille du texte (nb de mots présents) : {size_doc}")
print(f"Taille de la requête : {size_query}")
print(f"\nScore de Dice (manuel) = 2 * intersection / (|doc| + |query|) = {dice_manual:.4f}")
