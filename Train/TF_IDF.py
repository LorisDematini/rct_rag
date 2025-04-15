from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import euclidean_distances
import numpy as np
import math
from collections import Counter

# Données
texte1 = "test salut comment ça salut"
texte2 = "test coucou comment ça coucou salut"
texte3 = "test comment ça coucou"
documents = [texte1, texte2, texte3]
query = ["salut"]

print("Documents :", documents)


# === Partie 1 : TF-IDF avec sklearn ===
vectorizer = TfidfVectorizer(norm='l2')
X_docs = vectorizer.fit_transform(documents)
X_query = vectorizer.transform(query)

print("=== TF-IDF avec sklearn ===")
for i, vec in enumerate(X_docs.toarray()):
    print(f"Doc{i+1} :", vec)
print("\nVecteur de la requête :", X_query.toarray())

# === Partie 2 : Calcul TF-IDF à la main ===

# 1. Vocabulaire total
vocab = sorted(set(" ".join(documents).split()))
print("\nVocabulaire :", vocab)

# 2. Term Frequency (TF)
tf = []
for doc in documents:
    word_counts = Counter(doc.split())
    total = sum(word_counts.values())
    tf_doc = {word: word_counts[word] / total for word in vocab}
    tf.append(tf_doc)

print("\n=== TF ===")
for i, tf_doc in enumerate(tf):
    print(f"Doc{i+1} :", tf_doc)

# 3. Document Frequency (DF)
df = {word: sum(word in doc.split() for doc in documents) for word in vocab}

# 4. Inverse Document Frequency (IDF)
N = len(documents)
idf = {word: math.log((1 + N) / (1 + df[word])) + 1 for word in vocab}  # correction ici

print("\n=== IDF ===")
for word in vocab:
    print(f"{word} : {idf[word]:.4f}")

# 5. TF-IDF à la main (non normalisé)
manual_tfidf = []
for tf_doc in tf:
    tfidf_doc = {word: tf_doc[word] * idf[word] for word in vocab}
    manual_tfidf.append(tfidf_doc)

print("\n=== TF-IDF à la main (non normalisé) ===")
for i, tfidf_doc in enumerate(manual_tfidf):
    vec = [tfidf_doc[word] for word in vocab]
    print(f"Doc{i+1} :", vec)

# 6. Normalisation L2
normalized_manual_tfidf = []
for tfidf_doc in manual_tfidf:
    vec = np.array([tfidf_doc[word] for word in vocab])
    norm = np.linalg.norm(vec)
    if norm == 0:
        vec_normalized = vec
    else:
        vec_normalized = vec / norm
    normalized_manual_tfidf.append(vec_normalized)

print("\n=== TF-IDF à la main (normalisé L2) ===")
for i, vec in enumerate(normalized_manual_tfidf):
    print(f"Doc{i+1} :", vec)

# === Partie 3 : Distances euclidiennes avec sklearn ===
print("\n=== Distances euclidiennes avec sklearn ===")
for i, doc_vec in enumerate(X_docs.toarray()):
    d = euclidean_distances([X_query.toarray()[0]], [doc_vec])[0][0]
    print(f"Distance requête vs Doc{i+1} : {d:.4f}")