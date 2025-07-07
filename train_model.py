import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import joblib

# Load dataset
df = pd.read_csv("data.csv")

# Encode categorical variables
df["Gender"] = df["Gender"].map({"Male": 1, "Female": 0})
df["Team_Player"] = df["Team_Player"].map({"Yes": 1, "No": 0})

# Features and label
features = ["Age", "Gender", "Height_cm", "Weight_kg", "Endurance", "Aggression", "Team_Player"]
target = "Recommended_Sport"

# Split into X and y
X = df[features]
y = df[target]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the model
model = RandomForestClassifier()
model.fit(X_train, y_train)

# Save the model
joblib.dump(model, "sport_model.pkl")
print("✅ Model trained and saved as sport_model.pkl")
