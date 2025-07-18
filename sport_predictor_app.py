import streamlit as st
import pandas as pd
import joblib
import time
import os
import json
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

# Page Config
st.set_page_config(page_title="Zeitgeist", layout="wide")

# Custom CSS
st.markdown("""
<style>
    html, body, [class*="css"] {
        font-family: 'Times New Roman', serif;
        background: linear-gradient(to right, #1f8fff, #8e44ad);
        color: white;
    }
    .stApp {
        background: linear-gradient(145deg, #1f8fff, #ff0080, #8e44ad);
        background-size: 600% 600%;
        animation: gradientAnimation 15s ease infinite;
    }
    @keyframes gradientAnimation {
        0% {background-position: 0% 50%;}
        50% {background-position: 100% 50%;}
        100% {background-position: 0% 50%;}
    }
    .stButton > button {
        background-color: #1f8fff;
        color: white;
        border: none;
        border-radius: 12px;
        padding: 10px 20px;
        font-weight: bold;
        font-size: 16px;
        transition: background 0.3s ease;
    }
    .stButton > button:hover {
        background-color: #0d6efd;
    }
    .stSidebar {
        background: linear-gradient(to bottom, #3e8cff, #6200ea);
        color: white;
    }
    h1, h2, h3, h4 {
        font-family: 'Times New Roman', serif;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Typing animation
def fast_type(text):
    placeholder = st.empty()
    for i in range(1, len(text)+1):
        placeholder.markdown(text[:i])
        time.sleep(0.01)

# Load model
model = joblib.load("sport_model.pkl")

# Optional login system
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""

user_db_file = "user_db.json"
if not os.path.exists(user_db_file):
    with open(user_db_file, "w") as f:
        json.dump({}, f)
with open(user_db_file, "r") as f:
    user_db = json.load(f)

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

# Sidebar
page = st.sidebar.selectbox("Navigate", [
    "🏠 Home",
    "🎯 Zeitgeist AI",
    "📊 BMI Calculator",
    "🧬 Endurance Estimator",
    "💢 Aggression Scale",
    "🧠 Pro Plan"
])

# HOME PAGE
if page == "🏠 Home":
    st.title("🏠 Welcome to **Zeitgeist**")
    st.markdown("""
    This AI-powered app helps you discover your ideal sport and grow into a pro.

    **Features:**
    - 🎯 Sport Prediction (AI)
    - 📊 BMI Analyzer
    - 🧬 Endurance Test
    - 💢 Aggression Scale
    - 🧠 Step-by-step Pro Plan
    """)

# SPORT PREDICTOR
elif page == "🎯 Zeitgeist AI":
    st.title("🎯 Zeitgeist AI - Sport Predictor")
    age = st.slider("Age", 10, 60, 25)
    gender = st.selectbox("Gender", ["Male", "Female"])
    height = st.number_input("Height (cm)", 100, 250, 170)
    weight = st.number_input("Weight (kg)", 30, 200, 70)
    endurance = st.slider("Endurance (1 to 10)", 1, 10, 5)
    aggression = st.slider("Aggression (1 to 10)", 1, 10, 5)
    team_player = st.selectbox("Team Player?", ["Yes", "No"])

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
            fast_type(f"🏅 Recommended Sport: **{sport}**")

            st.markdown("---")
            st.subheader(f"💡 How to Become a Pro in {sport}")
            tips = {
                "Boxing": ["Join a certified boxing gym", "Daily training with bags/sparring", "Watch pro matches", "Compete in amateurs"],
                "Swimming": ["Hire a coach", "Swim 6 days/week", "Join competitions", "Track lap times weekly"],
                "Football": ["Join local club", "Practice shooting & dribbling", "Build stamina", "Attend open trials"],
                "Tennis": ["Learn serve & return", "Practice drills", "Join tournaments", "Use match videos for feedback"],
                "Wrestling": ["Mat drills daily", "Work on takedowns", "Study state-level rules", "Track diet & weight class"]
            }
            for tip in tips.get(sport, ["Practice regularly", "Set goals", "Join clubs", "Take feedback"]):
                st.markdown(f"- {tip}")

# BMI CALCULATOR
elif page == "📊 BMI Calculator":
    st.title("📊 BMI Calculator")
    height_cm = st.number_input("Height (cm)", 100, 250, 170)
    weight_kg = st.number_input("Weight (kg)", 30, 200, 70)

    if st.button("Calculate BMI"):
        height_m = height_cm / 100
        bmi = weight_kg / (height_m ** 2)
        st.success(f"Your BMI is **{bmi:.2f} kg/m²**")

        if bmi < 18.5:
            st.info("🟦 Underweight")
            st.warning("You are below the normal weight range.")
            st.markdown("""
            **Justification:** Lower BMI can lead to fatigue and poor immunity.
            **Try:** High-protein diet, calorie surplus, resistance workouts.
            """)
        elif bmi < 24.9:
            st.success("🟩 Normal")
            st.info("Great job! You're in the healthy range.")
            st.markdown("""
            **Justification:** Normal BMI is linked to lower risk of diseases.
            **Maintain:** Balanced diet, hydration, physical activity.
            """)
        elif bmi < 29.9:
            st.warning("🟧 Overweight")
            st.warning("You're slightly above normal BMI.")
            st.markdown("""
            **Justification:** Higher BMI may increase chances of diabetes and heart issues.
            **Try:** Cardio workouts, reduce sugar/oil, increase fiber.
            """)
        else:
            st.error("🟥 Obese")
            st.error("You are in the obese BMI range.")
            st.markdown("""
            **Justification:** Obesity increases risk for multiple chronic illnesses.
            **Try:** Consult a doctor, create a strict plan, cut junk food.
            """)

        st.markdown("### 📊 BMI Category Chart")
        categories = ["Underweight", "Normal", "Overweight", "Obese"]
        values = [18.4, 24.9, 29.9, 35]
        colors = ['skyblue', 'lightgreen', 'orange', 'red']
        fig, ax = plt.subplots()
        ax.bar(categories, values, color=colors)
        ax.axhline(bmi, color='blue', linestyle='--', label=f'Your BMI: {bmi:.2f}')
        ax.set_ylabel("BMI")
        ax.legend()
        st.pyplot(fig)

        st.markdown("### 🧭 BMI Gauge")
        fig, ax = plt.subplots(figsize=(6, 3))
        ax.axis('off')
        ax.annotate(f'{bmi:.2f} kg/m²', xy=(0.5, 0.6), ha='center', fontsize=24, color='white')

        theta = (bmi / 40) * 180
        x = [0.5, 0.5 + 0.4 * np.cos(np.radians(180 - theta))]
        y = [0.6, 0.6 + 0.4 * np.sin(np.radians(180 - theta))]
        ax.annotate('', xy=(x[1], y[1]), xytext=(x[0], y[0]), arrowprops=dict(facecolor='blue', width=4, headwidth=8))
        st.pyplot(fig)

# ENDURANCE ESTIMATOR
elif page == "🧬 Endurance Estimator":
    st.title("🧬 Endurance Estimator")
    q1 = st.slider("How long can you jog? (minutes)", 1, 60, 10)
    q2 = st.slider("Pushups in one set", 1, 100, 20)
    q3 = st.slider("Workouts per week", 0, 7, 3)
    score = round((q1/60)*0.4 + (q2/100)*0.3 + (q3/7)*0.3, 2)
    endurance = round(score * 10, 1)
    st.success(f"Estimated Endurance: **{endurance}/10**")

# AGGRESSION SCALE
elif page == "💢 Aggression Scale":
    st.title("💢 Aggression Assessment")
    q1 = st.slider("Do you get angry easily?", 1, 10, 5)
    q2 = st.slider("Do you confront people?", 1, 10, 5)
    q3 = st.slider("Do you enjoy competition?", 1, 10, 5)
    score = round((q1 + q2 + q3)/3, 1)
    st.success(f"Aggression Score: **{score}/10**")

# PRO PLAN PAGE
elif page == "🧠 Pro Plan":
    st.title("🧠 Your Pro Journey Plan")
    st.markdown("Let's plan your growth based on your available time:")
    time_avail = st.selectbox("How much time can you train per week?", [
        "1-3 hrs", "4-6 hrs", "7-10 hrs", "10+ hrs"
    ])

    if time_avail == "1-3 hrs":
        st.markdown("""
        - Focus on core skill once per week  
        - Use short 30-min drills  
        - Watch training videos to optimize time  
        """)
    elif time_avail == "4-6 hrs":
        st.markdown("""
        - 3 sessions/week (strength, skill, stamina)  
        - Log your progress weekly  
        - Join local competitions  
        """)
    elif time_avail == "7-10 hrs":
        st.markdown("""
        - 5 sessions/week with coach or structured plan  
        - Review nutrition and sleep  
        - Play in real matches or games  
        """)
    else:
        st.markdown("""
        - Full-time commitment: join academy  
        - Record and review sessions  
        - Compete at state/national level  
        - Get professional mentorship  
        """)

# CREDITS
st.markdown("""
---
#### 👨‍💻 Team Credits:
**Samvit**, **Satyaki**, **Varyam**, **Manu Sharth**, **Aarnav Tripathi**
""")
