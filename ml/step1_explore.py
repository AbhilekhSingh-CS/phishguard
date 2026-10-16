import pandas as pd

CSV_PATH = "Dataset.csv"

df = pd.read_csv(CSV_PATH)

print("Total rows:", df.shape[0])
print("Total columns:", df.shape[1])
print("\nColumn names:")
for col in df.columns:
    print(" -", col)

print("\nFirst 3 rows:")
print(df.head(3))

print("\nLabel column value counts:")
for col in df.columns:
    if df[col].nunique() <= 5:
        print(f"\n'{col}' column:")
        print(df[col].value_counts())
