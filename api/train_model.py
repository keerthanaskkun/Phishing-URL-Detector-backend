import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import pickle

# 1. Load the dataset
df = pd.read_excel("dataset_phishing.xlsx")

# 2. Clean whitespace and standardize label values
df['status'] = df['status'].str.strip().str.lower()

# 3. Encode labels (phishing = 1, legitimate = 0)
df['label'] = df['status'].apply(lambda x: 1 if x == 'phishing' else 0)

# 4. Drop unused columns (url + original status)
X = df.drop(columns=['url', 'status', 'label'])
y = df['label']

# 5. Train the model
model = RandomForestClassifier()
model.fit(X, y)

# 6. Save the model
with open('model.pkl', 'wb') as f:
    pickle.dump(model, f)

print("✅ Model retrained and saved as model.pkl")

