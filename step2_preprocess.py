import pandas as pd

df = pd.read_csv("Dataset.csv")

print("Original shape:", df.shape)

# Drop text columns - not useful for ML
df = df.drop(columns=['url', 'dom', 'tld'])

print("After dropping text columns:", df.shape)

# Check missing values
print("\nMissing values:", df.isnull().sum().sum())

# Save clean dataset
df.to_csv("clean_dataset.csv", index=False)

print("\nDone! Saved as clean_dataset.csv")
print("Columns kept:", df.columns.tolist())
print("\nLabel distribution:")
print(df['label'].value_counts())
