# model.py

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import joblib
import pickle

# Load data
df = pd.read_csv("data.csv")

# Features and label
X = df[['Age', 'Gender', 'Height_cm', 'Weight_kg', 'Endurance', 'Aggression', 'Team_Player']]
y = df['Recommended_Sport']

# Split the dataset
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Save the model
with open("sport_model.pkl", "wb") as f:
    pickle.dump(model, f)

print("✅ Model trained and saved as sport_model.pkl")
