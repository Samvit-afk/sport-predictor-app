import streamlit as st
import pandas as pd
import joblib
import time
import os
import json
import matplotlib.pyplot as plt

# --- Page Config ---
st.set_page_config(page_title="Sport Recommendation App", layout="wide")

# --- Custom CSS for UI ---
st.markdown("""
<style>
/* Main background gradient */
.stApp {
    background: linear-gradient(135deg, #00c6ff, #0072ff);
    color: white;
}

/* Sidebar panel background */
section[data-testid="stSidebar"] {
    background-color: #0091dd !important;
    color: white;
}

/* Button Styling */
div.stButton > button {
    background-color: #1f8fff;
    color: white;
    border-radius: 10px;
    padding: 0.6em 1.2em;
    font-weight: bold;
    font-size: 16px;
    border: none;
    transition: all 0.3s ease;
}
div.stButton > button:hover {
    background-color: #00c6ff;
    color: black;
}

h1, h2, h3, h4, h5, h6 {
    color: white;
}
</style>
""", unsafe_allow_html=True)

# --- Typing Animation ---
def typewriter_effect(text, speed=0.05):
    placeholder = st.empty()
    typed = ""
    for char in text:
        typed += char
        placeholder.markdown(f"🏅 **{typed}**")
        time.sleep(speed)

# --- Load model ---
model = joblib.load("sport_model.pkl")

# --- Session State ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""

# --- User DB ---
user_db_file = "user_db.json"
if not os.path.exists(user_db_file):
    with open(user_db_file, "w") as f:
        json.dump({}, f)
with open(user_db_file, "r") as f:
    user_db = json.load(f)

# --- Sidebar Auth ---
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
                st.success("Registration successful.")
    else:
        if st.button("Login"):
            if username in user_db and user_db[username] == password:
                st.session_state.logged_in = True
                st.session_state.username = username
                st.success("Logged in successfully.")
            else:
                st.error("Invalid credentials.")

if st.session_state.logged_in:
    st.sidebar.markdown(f"✅ Logged in as: **{st.session_state.username}**")
else:
    st.sidebar.markdown("👤 Not logged in")

# --- Navigation ---
page = st.sidebar.selectbox("Navigate", [
    "🏠 Home",
    "🎯 Predictor.AI",
    "📊 BMI Calculator",
    "🧬 Endurance Estimator",
    "💢 Aggression Scale",
    "🥗 Diet Planner"
])

# --- Pages ---
if page == "🏠 Home":
    st.title("🏠 Welcome to the Sport Recommender")
    st.markdown("""
    This app predicts the best sport for you based on your physical and behavioral attributes.

    **Features:**
    - AI-based Sport Recommendation
    - BMI Calculator with Tips & Chart
    - Endurance & Aggression Check
    - Personalized Diet Planner
    """)

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
            time.sleep(1.5)
            prediction = model.predict(input_df)
            sport = prediction[0]
            st.success("🏅 Recommended Sport:")
            typewriter_effect(sport, speed=0.05)
            if medical_condition:
                st.warning("⚠️ Note: Consult a doctor before playing any sport with your medical condition.")

elif page == "📊 BMI Calculator":
    st.title("📊 BMI Calculator")
    height_cm = st.number_input("Enter your height (cm):", 100, 250, 170)
    weight_kg = st.number_input("Enter your weight (kg):", 30, 200, 70)

    if st.button("Calculate BMI"):
        height_m = height_cm / 100
        bmi = weight_kg / (height_m ** 2)
        st.success(f"Your BMI is **{bmi:.2f}**")

        if bmi < 18.5:
            st.info("🟦 Category: **Underweight**")
            st.markdown("**Tips:** Eat high-calorie and protein-rich foods.")
        elif bmi < 24.9:
            st.success("🟩 Category: **Normal**")
            st.markdown("**Tips:** Keep up a balanced diet and active lifestyle.")
        elif bmi < 29.9:
            st.warning("🟧 Category: **Overweight**")
            st.markdown("**Tips:** Eat light, exercise more, reduce sugar.")
        else:
            st.error("🟥 Category: **Obese**")
            st.markdown("**Tips:** Follow a low-calorie diet and consult a doctor.")

        st.markdown("### 📊 BMI Category Comparison")
        categories = ["Underweight", "Normal", "Overweight", "Obese"]
        bmi_ranges = [18.4, 24.9, 29.9, 35]
        colors = ['skyblue', 'lightgreen', 'orange', 'red']

        fig, ax = plt.subplots()
        ax.bar(categories, bmi_ranges, color=colors)
        ax.axhline(bmi, color='blue', linestyle='--', label=f'Your BMI: {bmi:.2f}')
        ax.set_ylabel("BMI Value")
        ax.set_title("BMI Categories vs Your BMI")
        ax.legend()
        st.pyplot(fig)

elif page == "🧬 Endurance Estimator":
    st.title("🧬 Endurance Estimator")
    q1 = st.slider("How long can you jog without stopping? (mins)", 1, 60, 10)
    q2 = st.slider("How many pushups can you do in one set?", 1, 100, 20)
    q3 = st.slider("How often do you exercise weekly?", 0, 7, 3)
    est = (q1/60)*0.4 + (q2/100)*0.3 + (q3/7)*0.3
    endurance_score = round(est * 10, 1)
    st.success(f"Estimated Endurance Score: **{endurance_score}/10**")

elif page == "💢 Aggression Scale":
    st.title("💢 Aggression Assessment")
    q1 = st.slider("How often do you get angry easily?", 1, 10, 5)
    q2 = st.slider("How likely are you to confront someone when annoyed?", 1, 10, 5)
    q3 = st.slider("Do you enjoy competitive environments?", 1, 10, 5)
    aggression_score = round((q1 + q2 + q3) / 3, 1)
    st.success(f"Your Aggression Score: **{aggression_score}/10**")

elif page == "🥗 Diet Planner":
    st.title("🥗 Custom Diet Planner")
    weight = st.number_input("Current Weight (kg)", 30, 200, 70)
    target = st.number_input("Target Weight (kg)", 30, 200, 65)
    preference = st.selectbox("Diet Type", ["Balanced", "High Protein", "Vegetarian", "Low Carb"])

    if st.button("Generate Plan"):
        st.info("Generating meal plan...")
        time.sleep(2)
        if
