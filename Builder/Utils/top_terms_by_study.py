import json
import os
from Config import TOP_TERMS_PATH

def top_terms_per_document(vectorizer, sparse_matrix, study_ids, top_n=3):
    feature_names = vectorizer.get_feature_names_out()
    top_terms_dict = {}

    for i in range(sparse_matrix.shape[0]):
        row_dense = sparse_matrix[i].toarray().flatten()
        top_indices = row_dense.argsort()[::-1][:top_n]
        top_terms = [(feature_names[idx], row_dense[idx]) for idx in top_indices if row_dense[idx] > 0]
        top_terms_dict[study_ids[i]] = top_terms

    with open(TOP_TERMS_PATH, "w", encoding="utf-8") as f:
        json.dump(top_terms_dict, f, indent=2, ensure_ascii=False)

    print("Top termes stored in ", TOP_TERMS_PATH)
