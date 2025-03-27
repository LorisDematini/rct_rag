"""
Given an embeddings dictionnary and a query
- build a query embedding
- build a vector db based on embeddings dictionnary
- performs similarity search and returns the top k-results/distances computed
"""

from gen_embedding import *
import faiss

def vectordb(embeddings_dict) :
    embedding_dim = list(embeddings_dict.values())[0].shape[0]
    index = faiss.IndexFlatL2(embedding_dim)
    keys = list(embeddings_dict.keys()) #saves matching between dictionnary keys and faiss index 
    embedding_matrix = np.vstack([embeddings_dict[key] for key in keys]).astype('float32')
    index.add(embedding_matrix)
    return(index, keys)

def query_db(query_text, index, keys, top_k):

    query_embed = get_embedding_text(query_text).reshape(1, -1)

    #Search FAISS for the k most similar documents
    distances, indices = index.search(query_embed, top_k)

    matched_keys = [[keys[i] for i in idx_list] for idx_list in indices]

    return(distances,matched_keys)