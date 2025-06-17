import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import pickle

# Load the updated dataset
df = pd.read_csv("data.csv")

# Prepare features and target
X = df.drop("Recommended_Sport", axis=1)
y = df["Recommended_Sport"]

# Train the model
model = RandomForestClassifier()
model.fit(X, y)

# Save the trained model
with open("model.pkl", "wb") as f:
    pickle.dump(model, f)

print("✅ Model trained and saved successfully!")
