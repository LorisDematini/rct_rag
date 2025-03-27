######################
 
import pandas as pd
import sys
import os
import numpy as np
from tqdm import tqdm
import pickle

####################

sys.path.append(os.path.abspath("../config"))
sys.path.append(os.path.abspath("../rag"))
from config import configure_openai
configure_openai()
from gen_embedding import *
from query_vectordb import *

#####################


if __name__ == "__main__":


    df = pd.read_csv("C:/DonneesLocales/vsc/rag_project/rct_rag/systematic_review/data/dose_finding_review.csv")
    ### preprocessing
    df.dropna(subset=["abstract"], inplace=True)
    df["text"] = df["titre"] + df["abstract"]
    df = df[["record_id", "text"]]

    with open("data/embeddings.pkl", "rb") as f:
        embeddings_dict = pickle.load(f)

    query_text = "randomized dose-ranging clinical trials in oncology"

    n = len(list(embeddings_dict.keys()))
    print("number of abtracts treated :", n)

    db_index, keys = vectordb(embeddings_dict)

    distances, matched_keys = query_db(query_text, db_index, keys, n)
    matched_keys_list = matched_keys[0]
    distances_list = distances[0]
    # Create a mapping from key to distance
    key_distance_map = dict(zip(matched_keys_list, distances_list))

    # Filter the dataframe
    topk_df = df[df.record_id.isin(matched_keys_list)].copy()
    topk_df["distance"] = topk_df["record_id"].map(key_distance_map)
    topk_df[["record_id", "distance", "text"]].sort_values(by="distance", ascending = False).to_csv("data/topk_results.csv", index=False, sep=";")

    print("computed distance between query : ", query_text, "and top", n, "results")