######################
 
import pandas as pd
from sklearn.metrics import roc_curve, roc_auc_score, confusion_matrix
import matplotlib.pyplot as plt
import numpy as np

######################

results = pd.read_csv("C:/DonneesLocales/vsc/rag_project/rct_rag/systematic_review/data/results.csv")
print(len(results))

print(results.columns)

mapping = {"Exclusion" : 1, 
           "Full text reading" : 0}

results["outcome"] = results.decision_reviewer2.apply(lambda x : mapping[x])

df = pd.read_csv("C:/DonneesLocales/vsc/rag_project/rct_rag/systematic_review/data/topk_results.csv", sep=";")
print(len(df))

df = df.merge(results, on ="record_id", how = "left")

df = df[~df.outcome.isna()]
print(len(df))

print(df.distance.describe())

# Compute ROC curve
fpr, tpr, thresholds = roc_curve(df['outcome'], df['distance'])

# Optionally compute AUC
auc_score = roc_auc_score(df['outcome'], df['distance'])

# Plotting
plt.figure()
plt.plot(fpr, tpr, label=f'ROC Curve (AUC = {auc_score:.2f})')
plt.plot([0, 1], [0, 1], 'k--')  # Diagonal line for random guessing
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('ROC Curve')
plt.legend(loc='lower right')
plt.grid()
plt.savefig("img/res.png")

youden_j = tpr - fpr
optimal_idx = np.argmax(youden_j)
optimal_threshold = thresholds[optimal_idx]

df["prediction"] = df["distance"].apply(lambda x : 0 if x < optimal_threshold else 1)

cm = confusion_matrix(df["outcome"], df["prediction"])
cm_df = pd.DataFrame(cm, index=["Actual 0", "Actual 1"], columns=["Predicted 0", "Predicted 1"])

print(cm_df)