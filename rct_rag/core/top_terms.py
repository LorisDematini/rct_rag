"""
top_terms.py

Ce module gère l'extraction, le stockage et le chargement des mots les plus significatifs
(par score TF-IDF) pour chaque document du corpus.

Fonctions :
- save_top_terms(top_terms_dict) :
    Sauvegarde les top termes dans un fichier JSON.

- load_top_terms() :
    Charge les top termes depuis un fichier JSON s'il existe.

- top_terms_per_document(vectorizer, sparse_matrix, study_ids, top_n) :
    Calcule les `top_n` termes TF-IDF les plus pertinents pour chaque document.

- get_top_terms(vectorizer, sparse_matrix, study_ids) :
    Renvoie les top termes depuis le cache JSON, ou les calcule et les sauvegarde si absents.
"""

import json
import os
from config.settings import TOP_K_MOTS
from config.paths import TOP_TERMS_PATH

#On sauvegarde les top terms pour pas avoir à les retrouver à chaque lancement
def save_top_terms(top_terms_dict):
    print("Top termes sauvegardés")
    with open(TOP_TERMS_PATH, "w", encoding="utf-8") as f:
        json.dump(top_terms_dict, f, indent=2, ensure_ascii=False)

#On les charge
def load_top_terms():
    if not os.path.exists(TOP_TERMS_PATH):
        return None
    with open(TOP_TERMS_PATH, "r", encoding="utf-8") as f1:
        return json.load(f1)

#On trouve les top termes pour chaque étude
def top_terms_per_document(vectorizer, sparse_matrix, study_ids, top_n=TOP_K_MOTS):
    feature_names = vectorizer.get_feature_names_out()
    top_terms_dict = {}

    for i in range(sparse_matrix.shape[0]):
        row_dense = sparse_matrix[i].toarray().flatten()
        top_indices = row_dense.argsort()[::-1][:top_n]
        top_terms = [(feature_names[idx], row_dense[idx]) for idx in top_indices if row_dense[idx] > 0]
        top_terms_dict[study_ids[i]] = top_terms

    return top_terms_dict

#Fonction principale qui va appeler le téléchargement et si il n'existe pas, on le crée et le sauvegarde
def get_top_terms(vectorizer, sparse_matrix, study_ids):
    top_terms = load_top_terms()
    if top_terms is None:
        top_terms = top_terms_per_document(vectorizer, sparse_matrix, study_ids)
        save_top_terms(top_terms)
    return top_terms