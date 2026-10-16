import pandas as pd

df = pd.read_csv("clean_dataset.csv")

# Show some actual phishing URLs stats
phishing = df[df['label'] == 1]
legit = df[df['label'] == 0]

print("=== PHISHING URL FEATURE AVERAGES ===")
print(phishing.mean().round(3))

print("\n=== LEGIT URL FEATURE AVERAGES ===")
print(legit.mean().round(3))

print("\n=== BIGGEST DIFFERENCES ===")
diff = (phishing.mean() - legit.mean()).abs().sort_values(ascending=False)
print(diff.round(3))
