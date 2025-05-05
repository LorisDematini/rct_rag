from sentence_transformers import SentenceTransformer, util
from datasets import load_dataset
from scipy.stats import spearmanr
from tqdm import tqdm

# Modèles à comparer
model_names = [
    "sentence-transformers/all-MiniLM-L6-v2",
    "sentence-transformers/all-MiniLM-L12-v2",
    "sentence-transformers/all-mpnet-base-v2"
]

# Charger les données de test STS Benchmark
dataset = load_dataset("stsb_multi_mt", name="en", split="test")

# Préparer les paires et labels
sentences1 = dataset["sentence1"]
sentences2 = dataset["sentence2"]
labels = dataset["similarity_score"]  # score entre 0 et 5
labels = [score / 5.0 for score in labels]  # normalisation 0-1

# Benchmark loop
for model_name in model_names:
    print(f"\n🔍 Benchmarking: {model_name}")
    model = SentenceTransformer(model_name)
    
    scores = []
    for s1, s2 in tqdm(zip(sentences1, sentences2), total=len(sentences1)):
        emb1 = model.encode(s1, convert_to_tensor=True)
        emb2 = model.encode(s2, convert_to_tensor=True)
        similarity = util.cos_sim(emb1, emb2).item()
        scores.append(similarity)
    
    correlation = spearmanr(scores, labels).correlation
    print(f"📈 Spearman correlation: {correlation:.4f}")
    