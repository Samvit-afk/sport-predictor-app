import streamlit as st
import pandas as pd
import joblib
import time
import os
import json
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# Set up page config
st.set_page_config(page_title="Zeitgeist", layout="wide")

# Apply custom CSS for aesthetics
st.markdown("""
    <style>
        html, body, [class*="css"]  {
            font-family: 'Times New Roman';
            background: linear-gradient(to right, #1f8fff, #8e44ad);
            color: white;
        }
        .sidebar .sidebar-content {
            background: linear-gradient(to bottom, #1f8fff, #4b0082);
        }
        .stButton > button {
            background-color: #1f8fff;
            color: white;
            border-radius: 8px;
        }
        h1, h2, h3, h4 {
            font-weight: bold;
        }
    </style>
""", unsafe_allow_html=True)

# Load model
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

# Sidebar Login/Register
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

# Navigation
page = st.sidebar.selectbox("Navigate", [
    "🏠 Home",
    "🎯 Zeitgeist AI",
    "📊 BMI Calculator",
    "🗓 Pro Plan"
])

# Home Page
if page == "🏠 Home":
    st.markdown("""
    <h1 style='text-align: center;'>Zeitgeist</h1>
    <h3 style='text-align: center;'>The Ultimate AI Sport Recommender</h3>
    <p style='text-align: center;'>AI-powered recommendations to find the sport that fits YOU best.</p>
    """, unsafe_allow_html=True)

# Zeitgeist AI
elif page == "🎯 Zeitgeist AI":
    st.title("🎯 Zeitgeist AI")

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
            time.sleep(2)
            prediction = model.predict(input_df)
            sport = prediction[0]

            # Typing animation
            st.markdown("<h3>🏅 Recommended Sport:</h3>", unsafe_allow_html=True)
            st.write("")
            for word in f"{sport}".split():
                st.markdown(f"**{word}** ", unsafe_allow_html=True)
                time.sleep(0.2)

            if medical_condition:
                st.warning("⚠️ Note: Please consult a physician before engaging in physical activities with your medical condition.")

            # Short pro tips
            st.markdown("""
            ### 💡 Tips to Go Pro:
            - 🏋️ Train daily with discipline
            - 🧠 Study techniques and strategies
            - 🎯 Participate in competitions
            - 📚 Learn from top athletes
            - 👨‍🏫 Get a coach/mentor
            """)

# BMI Calculator
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
            st.warning("⚠️ Your BMI is below normal.")
            st.markdown("**Justification:** Low BMI may result in nutrient deficiencies, fatigue, or a weakened immune system.")
            st.markdown("""### 🛠️ What You Can Do:
- 🍽️ Eat calorie-rich foods (nuts, bananas, dairy, rice)
- 🥩 Add protein (eggs, paneer, legumes)
- 🏋️‍♀️ Strength training helps build muscle
- 💤 Sleep well and rest
- 👨‍⚕️ See a doctor if it's sudden weight loss
""")
        elif bmi < 24.9:
            st.success("🟩 Category: **Normal weight**")
            st.info("✅ Great! Your BMI is in the healthy range.")
            st.markdown("**Justification:** Normal BMI lowers the risk of chronic diseases and supports physical performance.")
            st.markdown("""### 🛠️ What You Can Do:
- 🥗 Maintain a balanced diet
- 🏃‍♂️ Stay physically active
- 💧 Drink lots of water
- 💤 Sleep 7–9 hours a day
""")
        elif bmi < 29.9:
            st.warning("🟧 Category: **Overweight**")
            st.warning("⚠️ Your BMI is slightly above normal.")
            st.markdown("**Justification:** Higher BMI increases risk of diabetes, joint issues, and hypertension.")
            st.markdown("""### 🛠️ What You Can Do:
- 🍎 Eat more fruits, veggies, whole grains
- 🏃‍♀️ Exercise 30–60 mins daily
- 🚫 Reduce fried and sugary foods
- 🧘 Try stress-reducing activities like yoga
""")
        else:
            st.error("🟥 Category: **Obese**")
            st.error("❗ Your BMI is in the obese range. Action is needed.")
            st.markdown("**Justification:** Obesity increases the risk of heart disease, stroke, and diabetes.")
            st.markdown("""### 🛠️ What You Can Do:
- 🥗 Follow a low-calorie, high-fiber diet
- 🏃‍♀️ Walk, swim, cycle regularly
- 🍽️ Avoid junk food and soda
- 🧠 Track meals using an app
- 👨‍⚕️ Visit a doctor or dietitian for guidance
""")

        st.markdown("### 📊 BMI Category Comparison")
        categories = ["Underweight", "Normal", "Overweight", "Obese"]
        bmi_ranges = [18.4, 24.9, 29.9, 35]
        colors = ['skyblue', 'lightgreen', 'orange', 'red']

        fig1, ax1 = plt.subplots()
        ax1.bar(categories, bmi_ranges, color=colors)
        ax1.axhline(bmi, color='blue', linestyle='--', label=f'Your BMI: {bmi:.2f}')
        ax1.set_ylabel("BMI Value")
        ax1.set_title("BMI Categories vs Your BMI")
        ax1.legend()
        st.pyplot(fig1)

        st.markdown("### 🎯 BMI Gauge")
        fig2, ax2 = plt.subplots(figsize=(5, 2))
        ax2.axis("off")
        labels = ["Underweight", "Normal", "Overweight", "Obese"]
        values = [16.5, 21.7, 27.4, 32.5]
        colors_gauge = ['skyblue', 'lightgreen', 'orange', 'red']
        ax2.barh([0], [35], color="lightgray", height=0.3)
        ax2.barh([0], [bmi], color="deepskyblue", height=0.3)
        for i, v in enumerate(values):
            ax2.text(v, 0.35, labels[i], ha='center', color=colors_gauge[i], fontsize=8)
        ax2.set_xlim([10, 35])
        st.pyplot(fig2)

        st.markdown("---")
        st.markdown("### 👥 Project By")
        st.markdown("**Samvit, Satyaki, Varyam, Manu Sharth, Aarnav Tripathi**")

# Pro Plan
elif page == "🗓 Pro Plan":
    st.title("🗓 Personalized Pro Plan")
    time_available = st.selectbox("How much time can you spare per day?", ["30 mins", "1 hour", "2+ hours"])

    if st.button("Generate My Plan"):
        if time_available == "30 mins":
            st.markdown("""
            ### 📘 30-Minute Daily Plan:
            - 10 mins: Warm-up and stretching
            - 10 mins: Skill practice
            - 10 mins: Cool-down and video analysis
            - 🧠 Tip: Use this for consistency and habit-building
            """)
        elif time_available == "1 hour":
            st.markdown("""
            ### 📗 1-Hour Daily Plan:
            - 15 mins: Warm-up + cardio
            - 20 mins: Sport-specific drills
            - 15 mins: Strength training
            - 10 mins: Stretch + recovery
            - ✅ Add weekend match play
            """)
        else:
            st.markdown("""
            ### 📕 Intensive 2+ Hours Plan:
            - 30 mins: Conditioning & strength
            - 45 mins: Drills + tactical gameplay
            - 30 mins: Match simulation + review
            - 15 mins: Cool-down, rehab, mental prep
            - 🔁 Weekly progress tracking
            """)
