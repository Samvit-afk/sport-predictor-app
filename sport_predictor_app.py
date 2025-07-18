import streamlit as st
import pandas as pd
import joblib
import time
import os
import json
import matplotlib.pyplot as plt

# Page config with royal blue aesthetic
st.set_page_config(page_title="Sport Recommender AI", layout="wide")

# Apply background gradient using custom HTML & CSS
st.markdown("""
<style>
body {
    background: linear-gradient(to right, #89CFF0, #1f8fff);
}
section.main > div { background-color: #f0f9ff; border-radius: 10px; padding: 1.5rem; }
.stButton > button {
    background-color: #1f8fff !important;
    color: white;
    border-radius: 8px;
    font-weight: bold;
}
[data-testid="stSidebar"] {
    background: linear-gradient(to bottom, #dbefff, #89CFF0);
}
</style>
""", unsafe_allow_html=True)

# Load trained model
model = joblib.load("sport_model.pkl")

# Session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""

# User DB setup
user_db_file = "user_db.json"
if not os.path.exists(user_db_file):
    with open(user_db_file, "w") as f:
        json.dump({}, f)
with open(user_db_file, "r") as f:
    user_db = json.load(f)

# Sidebar
with st.sidebar.expander("🔐 Login / Register (Optional)", expanded=False):
    option = st.radio("Select Option", ["Login", "Register"])
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if option == "Register":
        if st.button("Register"):
            if username in user_db:
                st.error("Username already exists.")
            else:
                user_db[username] = password
                with open(user_db_file, "w") as f:
                    json.dump(user_db, f)
                st.success("Registered.")
    else:
        if st.button("Login"):
            if username in user_db and user_db[username] == password:
                st.session_state.logged_in = True
                st.session_state.username = username
                st.success("Logged in!")
            else:
                st.error("Invalid credentials")

if st.session_state.logged_in:
    st.sidebar.markdown(f"✅ Logged in as: **{st.session_state.username}**")
else:
    st.sidebar.markdown("👤 Not logged in")

# Navigation
page = st.sidebar.selectbox("Navigate", [
    "🏠 Home", "🎯 Predictor.AI", "📊 BMI Calculator",
    "🧬 Endurance Estimator", "💢 Aggression Scale", "🥗 Diet Planner"
])

# Home Page
if page == "🏠 Home":
    st.title("🏠 Welcome to the Sport Recommender")
    st.markdown("""
    This AI-powered app recommends the best sport for you based on your attributes.

    **Features:**
    - 🎯 AI-based Sport Predictor
    - 📊 BMI Calculator + Visual Chart
    - 🧬 Endurance Estimator
    - 💢 Aggression Analyzer
    - 🥗 Custom Diet Plan Generator
    """)

# Predictor Page
elif page == "🎯 Predictor.AI":
    st.title("🎯 Sport Predictor")

    age = st.slider("Age", 10, 60, 25)
    gender = st.selectbox("Gender", ["Male", "Female"])
    height = st.number_input("Height (cm)", 100, 250, 170)
    weight = st.number_input("Weight (kg)", 30, 200, 70)
    endurance = st.slider("Endurance (1 to 10)", 1, 10, 5)
    aggression = st.slider("Aggression (1 to 10)", 1, 10, 5)
    team_player = st.selectbox("Team Player?", ["Yes", "No"])
    medical_condition = st.text_input("Any medical condition (optional)")

    gender_val = 1 if gender == "Male" else 0
    team_val = 1 if team_player == "Yes" else 0

    input_df = pd.DataFrame([{
        "Age": age,
        "Gender": gender_val,
        "Height_cm": height,
        "Weight_kg": weight,
        "Endurance": endurance,
        "Aggression": aggression,
        "Team_Player": team_val
    }])

    if st.button("Predict Sport"):
        with st.spinner("Analyzing your profile..."):
            time.sleep(1)
            prediction = model.predict(input_df)
            sport = prediction[0]

        result_placeholder = st.empty()
        animated_text = f"🏅 Recommended Sport: **{sport}**"
        for i in range(len(animated_text)):
            result_placeholder.markdown(animated_text[:i+1])
            time.sleep(0.02)

        if medical_condition:
            st.warning("⚠️ Consult a doctor before participating in physical activities.")

# BMI Page
elif page == "📊 BMI Calculator":
    st.title("📊 BMI Calculator")
    h = st.number_input("Height (cm)", 100, 250, 170)
    w = st.number_input("Weight (kg)", 30, 200, 70)

    if st.button("Calculate BMI"):
        bmi = w / ((h / 100) ** 2)
        st.success(f"Your BMI is **{bmi:.2f}**")

        if bmi < 18.5:
            st.info("🟦 Underweight")
            st.markdown("- Eat calorie-dense foods\n- Exercise\n- Sleep well")
        elif bmi < 24.9:
            st.success("🟩 Normal weight")
            st.markdown("- Maintain your current routine!")
        elif bmi < 29.9:
            st.warning("🟧 Overweight")
            st.markdown("- Exercise daily\n- Avoid sugar & junk food")
        else:
            st.error("🟥 Obese")
            st.markdown("- Consult a dietitian\n- Focus on cardio & diet")

        # Chart
        st.markdown("### 📊 BMI Category Comparison")
        fig, ax = plt.subplots()
        cat = ["Underweight", "Normal", "Overweight", "Obese"]
        val = [18.4, 24.9, 29.9, 35]
        clr = ['skyblue', 'lightgreen', 'orange', 'red']
        ax.bar(cat, val, color=clr)
        ax.axhline(bmi, color='blue', linestyle='--', label=f'Your BMI: {bmi:.2f}')
        ax.legend()
        ax.set_ylabel("BMI Value")
        st.pyplot(fig)

# Endurance
elif page == "🧬 Endurance Estimator":
    st.title("🧬 Endurance Estimator")
    q1 = st.slider("Jog without stopping? (mins)", 1, 60, 10)
    q2 = st.slider("Pushups in one set", 1, 100, 20)
    q3 = st.slider("Days you exercise/week", 0, 7, 3)
    score = (q1/60)*0.4 + (q2/100)*0.3 + (q3/7)*0.3
    st.success(f"Estimated Endurance Score: **{round(score*10, 1)}/10**")

# Aggression
elif page == "💢 Aggression Scale":
    st.title("💢 Aggression Assessment")
    a1 = st.slider("Do you get angry easily?", 1, 10, 5)
    a2 = st.slider("Confront people when annoyed?", 1, 10, 5)
    a3 = st.slider("Like competitive settings?", 1, 10, 5)
    a_score = round((a1 + a2 + a3) / 3, 1)
    st.success(f"Your Aggression Score: **{a_score}/10**")

# Diet Planner
elif page == "🥗 Diet Planner":
    st.title("🥗 Custom Diet Planner")
    weight = st.number_input("Current Weight (kg)", 30, 200, 70)
    target = st.number_input("Target Weight (kg)", 30, 200, 65)
    preference = st.selectbox("Diet Type", ["Balanced", "High Protein", "Vegetarian", "Low Carb"])

    if st.button("Generate Plan"):
        st.info("Generating personalized meal plan...")
        time.sleep(1.5)
        goal = "lose" if target < weight else "gain" if target > weight else "maintain"
        st.success(f"To **{goal} weight**, try this {preference} diet:")

        if preference == "Balanced":
            st.markdown("- Oatmeal, banana, eggs\n- Brown rice, veggies, paneer\n- Fruits, yogurt")
        elif preference == "High Protein":
            st.markdown("- Eggs, nuts, protein shake\n- Tofu, lentils\n- Chicken, spinach")
        elif preference == "Vegetarian":
            st.markdown("- Veg pulao, dal, roti\n- Avocado toast, raita\n- Fruits, buttermilk")
        else:
            st.markdown("- Eggs, avocado\n- Chicken/fish + greens\n- Nuts, cheese")

        st.info("📥 Save/export options coming soon (login required)")
