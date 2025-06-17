import streamlit as st
import pandas as pd

import pickle

# Load model
with open("model.pkl", "rb") as f:
    model = pickle.load(f)

# UI
st.title("🏅 AI Sport Recommender")

st.markdown("### Enter your details:")

# Match these exactly with the new dataset features
height = st.number_input("Height (cm)")
weight = st.number_input("Weight (kg)")
agility = st.slider("Agility (0-10)", 0, 10, 5)
reaction_time = st.slider("Reaction Time (0-10)", 0, 10, 5)
gender = st.selectbox("Gender", ["Male", "Female"])

# Convert gender to numeric
gender_val = 1 if gender == "Male" else 0

# Prepare input
input_df = pd.DataFrame([{
    "Height_cm": height,
    "Weight_kg": weight,
    "Agility": agility,
    "Reaction_Time": reaction_time,
    "Gender": gender_val
}])

# Predict
if st.button("Recommend Sport"):
    prediction = model.predict(input_df)
    st.success(f"🏆 Recommended Sport: {prediction[0]}")

from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

# Load dataset
df = pd.read_csv("sport_dataset.csv")

# Features and target
X = df.drop("Sport", axis=1)
y = df["Sport"]

# Train model
model = DecisionTreeClassifier()
model.fit(X, y)

# App UI
st.set_page_config(page_title="Sport Recommender AI", layout="centered")
st.title("🏆 Sport Recommendation AI")
st.markdown("Enter your physical attributes to find out which sport suits you best!")

# User input
# User input - now using fillable fields
strength = st.number_input("Strength (1-10)", min_value=1, max_value=10, step=1)
speed = st.number_input("Speed (1-10)", min_value=1, max_value=10, step=1)
endurance = st.number_input("Endurance (1-10)", min_value=1, max_value=10, step=1)
agility = st.number_input("Agility (1-10)", min_value=1, max_value=10, step=1)
height = st.number_input("Height (in cm)", min_value=140, max_value=220, step=1)
weight = st.number_input("Weight (in kg)", min_value=40, max_value=150, step=1)
flexibility = st.number_input("Flexibility (1-10)", min_value=1, max_value=10, step=1)
balance = st.number_input("Balance (1-10)", min_value=1, max_value=10, step=1)

# Prediction
if st.button("Predict My Sport"):
    input_data = [[strength, speed, endurance, agility, height, weight, flexibility, balance]]
    prediction = model.predict(input_data)
    st.success(f"🏅 You are best suited for: **{prediction[0]}**!")
