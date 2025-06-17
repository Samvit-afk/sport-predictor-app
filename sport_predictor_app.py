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
