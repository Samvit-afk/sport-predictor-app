# train_model.py
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import pickle

# Load your data
data = pd.read_csv('sport_dataset.csv')

# Example: drop 'Sport' as the label, rest are features
X = data.drop('Sport', axis=1)
y = data['Sport']

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train a model
model = RandomForestClassifier()
model.fit(X_train, y_train)

# Save the model to model.pkl
with open('model.pkl', 'wb') as f:
    pickle.dump(model, f)

print("✅ Model trained and saved to model.pkl")
