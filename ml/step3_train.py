import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
from sklearn.preprocessing import StandardScaler
import pickle

# Load clean data
df = pd.read_csv("clean_dataset.csv")
print("Dataset loaded:", df.shape)

# Separate features and label
X = df.drop(columns=['label'])
y = df['label']

print("Features:", X.shape[1])
print("Training samples:", len(X))

# Split into train and test
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)
print("\nTrain size:", len(X_train))
print("Test size:", len(X_test))

# Scale the features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)
print("\nScaling done!")

# Train the model
print("\nTraining Random Forest... (this takes 1-2 minutes)")
model = RandomForestClassifier(
    n_estimators=200,
    random_state=42,
    n_jobs=-1,
    class_weight={0: 1, 1: 15},
    max_depth=None,
    min_samples_leaf=1
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

# Save model files
feature_names = X.columns.tolist()

with open("model.pkl", "wb") as f:
    pickle.dump(model, f)
with open("scaler.pkl", "wb") as f:
    pickle.dump(scaler, f)
with open("feature_names.pkl", "wb") as f:
    pickle.dump(feature_names, f)

print("\nSaved: model.pkl, scaler.pkl, feature_names.pkl")
print("\nDone! Next step: run the API.")
