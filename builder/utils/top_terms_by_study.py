import json
from typing import List
from config import TOP_TERMS_PATH

def top_terms_per_document(vectorizer, sparse_matrix, study_ids: List[str], top_n: int = 3) -> None:
    """
    Extract the top N terms with the highest TF-IDF scores for each document
    and save them to a JSON file.

    vectorizer: A fitted TfidfVectorizer instance.
    sparse_matrix: The document-term matrix (sparse format) from the vectorizer.
    study_ids (List[str]): List of document identifiers, one per row in the matrix.
    top_n (int, optional): Number of top terms to extract per document. Defaults to 3.
    """

    # Get all terms from the vectorizer vocabulary
    feature_names = vectorizer.get_feature_names_out()

    # Dictionary to store top terms for each document
    top_terms_dict = {}

    # Iterate over each row/document in the sparse matrix
    for i in range(sparse_matrix.shape[0]):
        # Convert sparse row to dense array
        row_dense = sparse_matrix[i].toarray().flatten()

        # Get indices of top N terms (with highest TF-IDF scores)
        top_indices = row_dense.argsort()[::-1][:top_n]

        # Extract corresponding terms and their scores
        top_terms = [
            (feature_names[idx], row_dense[idx])
            for idx in top_indices if row_dense[idx] > 0
        ]

        # Map the result to the corresponding study ID
        top_terms_dict[study_ids[i]] = top_terms

    # Write the top terms dictionary to JSON file
    with open(TOP_TERMS_PATH, "w", encoding="utf-8") as f:
        json.dump(top_terms_dict, f, indent=2, ensure_ascii=False)

    # Print final
    print("Top terms stored in", TOP_TERMS_PATH)