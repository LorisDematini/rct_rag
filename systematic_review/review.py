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

    # query_text = "randomized dose-ranging clinical trials in oncology"

    # query_text = "New classes of therapeutics in oncology emerged over the last decades but these new therapeutics (immunotherapies, target therapies, …) do not respect this assumption made for cytotoxic chemotherapies with prolonged effects, observation windows and delayed effects. There is thus a regain in interest for dose-ranging studies, especially in oncology in order to investigate several potential doses of the same drug in a phase II trial. In this context, we can use dose ranging studies in phase II to compare the efficacy of multiple doses (but less than in phase I) of the same drug. To our knowledge, there is no systematic review about how dose-ranging studies are analyzed in oncology."

    query_text = "Randomized phase II dose-ranging clinical trials in oncology that randomizes several doses of the same drug"# exclude methodological articles, exclude reanalyses of published data, exclude articles on not therapeutic drugs in cancer, exclude articles on other condition than cancer"

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
    topk_df[["record_id", "distance", "text"]].sort_values(by="distance").to_csv("data/topk_results.csv", index=False, sep=";") #the lower the distance, the best match is

    print("computed distance between query : ", query_text, "and top", n, "results")

