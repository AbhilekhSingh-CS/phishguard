import pandas as pd
from scipy.io import arff
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
import pickle

# The 14 features we can actually compute from a URL string alone.
# Everything else needs a WHOIS lookup, a DNS query, or fetching the page.
URL_ONLY_FEATURES = [
    "having_IP_Address",
    "URL_Length",
    "Shortining_Service",
    "having_At_Symbol",
    "double_slash_redirecting",
    "Prefix_Suffix",
    "having_Sub_Domain",
    "SSLfinal_State",
    "port",
    "HTTPS_token",
    "Submitting_to_email",
    "Abnormal_URL",
    "Redirect",
    "Statistical_report",
]

print("Loading UCI dataset...")
data, meta = arff.loadarff("uci_dataset.arff")
df = pd.DataFrame(data)

for col in df.columns:
    df[col] = df[col].astype(int)

print("Full dataset shape:", df.shape)

# Keep only the computable features
X = df[URL_ONLY_FEATURES]
y = df["Result"]

# UCI encodes phishing as -1 and legitimate as 1.
# Flip it so phishing = 1, because sklearn treats 1 as the positive class.
y = (y == -1).astype(int)

print("Using", X.shape[1], "features instead of 30")
print("\nLabel counts (1 = phishing, 0 = legitimate):")
print(y.value_counts())

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)
print("\nTrain size:", len(X_train))
print("Test size:", len(X_test))

# No scaling. Random Forest splits on thresholds, so feature scale is irrelevant.
print("\nTraining Random Forest...")
model = RandomForestClassifier(
    n_estimators=200,
    random_state=42,
    n_jobs=-1,
    class_weight="balanced",
)
model.fit(X_train, y_train)
print("Training complete!")

y_pred = model.predict(X_test)

acc = accuracy_score(y_test, y_pred)
prec = precision_score(y_test, y_pred)
rec = recall_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)

print("\n=============================")
print("   URL-ONLY MODEL RESULTS")
print("=============================")
print(f"Accuracy  : {acc*100:.2f}%")
print(f"Precision : {prec*100:.2f}%")
print(f"Recall    : {rec*100:.2f}%")
print(f"F1 Score  : {f1*100:.2f}%")
print("=============================")

cm = confusion_matrix(y_test, y_pred)
print("\nConfusion Matrix:")
print(f"  Correct Legit   : {cm[0][0]}")
print(f"  False Alarms    : {cm[0][1]}")
print(f"  Missed Phishing : {cm[1][0]}")
print(f"  Caught Phishing : {cm[1][1]}")

print("\nFeature importance (what the model actually relies on):")
importances = sorted(
    zip(URL_ONLY_FEATURES, model.feature_importances_),
    key=lambda x: x[1],
    reverse=True,
)
for rank, (feat, imp) in enumerate(importances, 1):
    print(f"  {rank:2}. {feat:<28} {imp:.4f}")

# Sanity check: does a clean, legitimate-looking URL score low?
clean_url_vector = pd.DataFrame(
    [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1]], columns=URL_ONLY_FEATURES
)
prob = model.predict_proba(clean_url_vector)[0][1]
print(f"\nSanity check - a clean legitimate-style URL scores {prob:.3f} phishing probability")
print("(should be low, well under 0.5)")

with open("model_urlonly.pkl", "wb") as f:
    pickle.dump(model, f)
with open("feature_names_urlonly.pkl", "wb") as f:
    pickle.dump(URL_ONLY_FEATURES, f)

print("\nSaved: model_urlonly.pkl, feature_names_urlonly.pkl")
print("Done!")