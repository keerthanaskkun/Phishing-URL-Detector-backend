import pandas as pd

df = pd.read_excel("dataset_phishing.xlsx")

print("📄 Columns:", df.columns.tolist())
print("🔍 Sample rows:\n", df.head())
print("🔢 Count of non-NaN in 'status':", df['status'].notna().sum())
