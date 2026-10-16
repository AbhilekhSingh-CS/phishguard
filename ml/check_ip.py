import pandas as pd
from scipy.io import arff

data, meta = arff.loadarff("uci_dataset.arff")
df = pd.DataFrame(data)
for col in df.columns:
    df[col] = df[col].astype(int)

ip_rows = df[df["having_IP_Address"] == -1]
print("URLs with an IP address:", len(ip_rows))
print(ip_rows["Result"].value_counts())