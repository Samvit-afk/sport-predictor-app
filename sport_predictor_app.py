import streamlit as st
import pandas as pd
import joblib
import time
import os
import json
import matplotlib.pyplot as plt

# Set custom page config
st.set_page_config(page_title="Sport Predictor", layout="wide")

# Neon gradient custom CSS styling
st.markdown("""
    <style>
    /* Background Gradient */
    body, .stApp {
        background: linear-gradient(135deg, #1f8fff, #ff00c8, #6f00ff);
        background-size: 600% 600%;
        animation: gradientFlow 15s ease infinite;
        color: white;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1f8fff, #6f00ff);
        color: white;
    }

    /* Neon buttons */
    .stButton>button {
        background-color: #1f8fff !important;
        color: white !important;
        border-radius: 10px;
        padding: 0.5em 1em;
        font-weight: bold;
        box-shadow: 0 0 10px #1f8fff;
        transition: 0.3s ease;
    }
    .stButton>button:hover {
        box-shadow: 0 0 20px #1f8fff;
    }

    @keyframes gradientFlow {
        0%{background-position:0% 50%}
        50%{background-position:100% 50%}
        100%{background-position:0% 50%}
    }
    </style>
""", unsafe_allow_html=True)

# Typing animation function
def type_text(message, delay=0.02):
    typed = ""
    message_placeholder = st.empty()
    for char in message:
        typed += char
        message_placeholder.markdown(f"**{typed}**")
        time.sleep(delay)

# Load model
model = joblib.load("sport_model.pkl")

# User DB
user_db_file = "user_db.json"
if not os.path.exists(user_db_file):
    with open(user_db_file, "w") as f:
        json.dump({}, f)
with open(user_db_file, "r") as f:
    user_db = json.load(f)

# Session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""

# Sidebar Login/Register
with st.sidebar.expander("🔐 Login / Register (Optional)", expanded=False):
    option = st.radio("Select Option", ["Login", "Register"])
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if option == "Register" and st.button("Register"):
        if username in user_db:
            st.error("Username already exists.")
        else:
            user_db[username] = password
            with open(user_db_file, "w") as f:
                json.dump(user_db, f)
            st.success("Registered.")
    elif option == "Login" and st.button("Login"):
        if username in user_db and user_db[username] == password:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.success("Logged in.")
        else:
            st.error("Invalid credentials.")

# Sidebar status
if st.session_state.logged_in:
    st.sidebar.markdown(f"✅ Logged in as: **{st.session_state.username}**")
else:
    st.sidebar.markdown("👤 Not logged in")

# Navigation
page = st.sidebar.selectbox("Navigate", [
    "🏠 Home",
    "🎯 Predictor.AI",
    "📊 BMI Calculator",
    "🧬 Endurance Estimator",
    "💢 Aggression Scale",
    "🥗 Diet Planner"
])

# Home
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

# Predictor
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
            prediction = model.predict(input_df)[0]
            type_text(f"🏅 Recommended Sport: **{prediction}**")
            if medical_condition:
                st.warning("⚠️ Please consult a doctor before physical activity.")

# BMI Calculator
elif page == "📊 BMI Calculator":
    st.title("📊 BMI Calculator")
    h = st.number_input("Height (cm)", 100, 250, 170)
    w = st.number_input("Weight (kg)", 30, 200, 70)

    if st.button("Calculate BMI"):
        h_m = h / 100
        bmi = w / (h_m ** 2)
        st.success(f"Your BMI is **{bmi:.2f}**")

        if bmi < 18.5:
            type_text("🟦 Category: Underweight")
            st.markdown("- Eat more calories and protein\n- Strength training\n- Sleep well")
        elif bmi < 24.9:
            type_text("🟩 Category: Normal")
            st.markdown("- Maintain a balanced diet\n- Keep active")
        elif bmi < 29.9:
            type_text("🟧 Category: Overweight")
            st.markdown("- Eat more fruits & veggies\n- Daily exercise\n- Reduce sugar")
        else:
            type_text("🟥 Category: Obese")
            st.markdown("- Low-calorie diet\n- Regular activity\n- Visit a doctor")

        st.markdown("### 📊 BMI Chart")
        fig, ax = plt.subplots()
        ax.bar(["Underweight", "Normal", "Overweight", "Obese"],
               [18.4, 24.9, 29.9, 35],
               color=['skyblue', 'green', 'orange', 'red'])
        ax.axhline(bmi, color='blue', linestyle='--', label=f'Your BMI: {bmi:.2f}')
        ax.legend()
        st.pyplot(fig)

# Endurance
elif page == "🧬 Endurance Estimator":
    st.title("🧬 Endurance Estimator")
    q1 = st.slider("Jog (mins)", 1, 60, 10)
    q2 = st.slider("Pushups (1 set)", 1, 100, 20)
    q3 = st.slider("Days active weekly", 0, 7, 3)
    score = (q1/60)*0.4 + (q2/100)*0.3 + (q3/7)*0.3
    type_text(f"🧪 Estimated Endurance Score: {round(score*10,1)}/10")

# Aggression
elif page == "💢 Aggression Scale":
    st.title("💢 Aggression Scale")
    a1 = st.slider("Get angry easily?", 1, 10, 5)
    a2 = st.slider("Confront when annoyed?", 1, 10, 5)
    a3 = st.slider("Enjoy competition?", 1, 10, 5)
    score = round((a1 + a2 + a3)/3, 1)
    type_text(f"🔥 Aggression Score: {score}/10")

# Diet
elif page == "🥗 Diet Planner":
    st.title("🥗 Diet Planner")
    cw = st.number_input("Current Weight (kg)", 30, 200, 70)
    tw = st.number_input("Target Weight (kg)", 30, 200, 65)
    plan = st.selectbox("Diet Type", ["Balanced", "High Protein", "Vegetarian", "Low Carb"])

    if st.button("Generate Plan"):
        time.sleep(1)
        action = "gain" if tw > cw else "lose" if tw < cw else "maintain"
        type_text(f"🎯 You want to {action} weight. Here's a {plan.lower()} diet:")

        if plan == "Balanced":
            st.markdown("- 🥣 Oats + banana + eggs\n- 🍛 Rice + chicken + salad\n- 🍽️ Chapati + paneer")
        elif plan == "High Protein":
            st.markdown("- 🍳 Eggs + shake + nuts\n- 🍛 Quinoa + lentils\n- 🥩 Chicken + veggies")
        elif plan == "Vegetarian":
            st.markdown("- 🍞 Toast + avocado\n- 🍛 Veg pulao + raita\n- 🍲 Dal + roti")
        else:
            st.markdown("- 🍳 Eggs + avocado\n- 🥗 Chicken/fish + salad\n- 🧀 Paneer + spinach")
