from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
import pickle

# Load dataset
df = pd.read_excel("dataset_phishing.xlsx")
df.dropna(inplace=True)

# Features and label
X = df.drop(columns=["status", "url"])
y = df["status"].map({'legitimate': 0, 'phishing': 1})  # convert to binary

# Split into training (80%) and test (20%)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = RandomForestClassifier()
model.fit(X_train, y_train)

# Evaluate model
y_pred = model.predict(X_test)
print(classification_report(y_test, y_pred))

# Save model
with open('model.pkl', 'wb') as f:
    pickle.dump(model, f)

print("✅ Model retrained and saved as model.pkl")
