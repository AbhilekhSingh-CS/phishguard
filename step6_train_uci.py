import pandas as pd
import numpy as np
from scipy.io import arff
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
from sklearn.preprocessing import StandardScaler
import pickle

# Load ARFF file
print("Loading UCI dataset...")
data, meta = arff.loadarff("uci_dataset.arff")
df = pd.DataFrame(data)

# Convert bytes to int
for col in df.columns:
    df[col] = df[col].astype(int)

print("Shape:", df.shape)
print("\nLabel distribution:")
print(df['Result'].value_counts())

# Features and label
X = df.drop(columns=['Result'])
y = df['Result']

# Convert -1/1 to 0/1
y = (y == -1).astype(int)  # -1 = phishing = 1, 1 = legit = 0
print("\nConverted labels:")
print(y.value_counts())

feature_names = X.columns.tolist()
print("\nFeatures:", feature_names)

# Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)
print("\nTrain size:", len(X_train))
print("Test size:", len(X_test))

# Scale
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled  = scaler.transform(X_test)

# Train
print("\nTraining Random Forest...")
model = RandomForestClassifier(
    n_estimators=200,
    random_state=42,
    n_jobs=-1,
    class_weight='balanced'
)
model.fit(X_train_scaled, y_train)
print("Training complete!")

# Evaluate
y_pred = model.predict(X_test_scaled)
acc  = accuracy_score(y_test, y_pred)
prec = precision_score(y_test, y_pred)
rec  = recall_score(y_test, y_pred)
f1   = f1_score(y_test, y_pred)

print("\n=============================")
print("       MODEL RESULTS")
print("=============================")
print(f"Accuracy  : {acc*100:.2f}%")
print(f"Precision : {prec*100:.2f}%")
print(f"Recall    : {rec*100:.2f}%")
print(f"F1 Score  : {f1*100:.2f}%")
print("=============================")

cm = confusion_matrix(y_test, y_pred)
print(f"\nConfusion Matrix:")
print(f"  Correct Legit   : {cm[0][0]}")
print(f"  False Alarms    : {cm[0][1]}")
print(f"  Missed Phishing : {cm[1][0]}")
print(f"  Caught Phishing : {cm[1][1]}")

# Feature importance
print("\nTop 10 Most Important Features:")
importances = model.feature_importances_
feat_imp = sorted(zip(feature_names, importances), key=lambda x: x[1], reverse=True)
for rank, (feat, imp) in enumerate(feat_imp[:10], 1):
    print(f"  {rank:2}. {feat:<35} {imp:.4f}")

# Save
with open("model.pkl", "wb") as f:
    pickle.dump(model, f)
with open("scaler.pkl", "wb") as f:
    pickle.dump(scaler, f)
with open("feature_names.pkl", "wb") as f:
    pickle.dump(feature_names, f)

print("\nSaved: model.pkl, scaler.pkl, feature_names.pkl")
print("Done!")
