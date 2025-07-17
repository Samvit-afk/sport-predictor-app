import streamlit as st
import pandas as pd
import joblib
import time
import os
import json
import matplotlib.pyplot as plt

# Set up page config
st.set_page_config(page_title="Sport Recommendation App", layout="wide")

# Load model
model = joblib.load("sport_model.pkl")

# Initialize session state
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

# --- Sidebar Login/Register ---
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
    "🎯 Predictor.AI",
    "📊 BMI Calculator",
    "🧬 Endurance Estimator",
    "💢 Aggression Scale",
    "🥗 Diet Planner"
])

# Page: Home
if page == "🏠 Home":
    st.title("🏠 Welcome to the Sport Recommender")
    st.markdown("""
    This app predicts the best sport for you based on your physical and behavioral attributes.

    **Features:**
    - AI-based Sport Recommendation
    - BMI Calculator
    - Endurance Estimator
    - Aggression Level Check
    - Personalized Diet Planner

    You can optionally log in to save personalized diet plans in the future.
    """)

# Page: Predictor
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
            time.sleep(2)
            prediction = model.predict(input_df)
            sport = prediction[0]
            st.success(f"🏅 Recommended Sport: **{sport}**")

            if medical_condition:
                st.warning("⚠️ Note: Please consult a physician before engaging in physical activities with your medical condition.")

# Page: BMI Calculator
elif page == "📊 BMI Calculator":
    st.title("📊 BMI Calculator")
    height_cm = st.number_input("Enter your height (cm):", 100, 250, 170)
    weight_kg = st.number_input("Enter your weight (kg):", 30, 200, 70)

    if st.button("Calculate BMI"):
        height_m = height_cm / 100
        bmi = weight_kg / (height_m ** 2)
        st.success(f"Your BMI is **{bmi:.2f}**")

        # Determine category and give tips
        if bmi < 18.5:
            st.info("🟦 Category: **Underweight**")
            st.warning("⚠️ Your BMI is below normal.")
            st.markdown("""
            ### 🛠️ What You Can Do:
            - 🍽️ Eat calorie-rich foods (nuts, bananas, dairy, rice)
            - 🥩 Add protein (eggs, paneer, legumes)
            - 🏋️‍♀️ Strength training helps build muscle
            - 💤 Sleep well and rest
            - 👨‍⚕️ See a doctor if it's sudden weight loss
            """)
        elif bmi < 24.9:
            st.success("🟩 Category: **Normal weight**")
            st.info("✅ Great! Your BMI is in the healthy range.")
            st.markdown("""
            ### 🛠️ What You Can Do:
            - 🥗 Maintain a balanced diet
            - 🏃‍♂️ Stay physically active
            - 💧 Drink lots of water
            - 💤 Sleep 7–9 hours a day
            """)
        elif bmi < 29.9:
            st.warning("🟧 Category: **Overweight**")
            st.warning("⚠️ Your BMI is slightly above normal.")
            st.markdown("""
            ### 🛠️ What You Can Do:
            - 🍎 Eat more fruits, veggies, whole grains
            - 🏃‍♀️ Exercise 30–60 mins daily
            - 🚫 Reduce fried and sugary foods
            - 🧘 Try stress-reducing activities like yoga
            """)
        else:
            st.error("🟥 Category: **Obese**")
            st.error("❗ Your BMI is in the obese range. Action is needed.")
            st.markdown("""
            ### 🛠️ What You Can Do:
            - 🥗 Follow a low-calorie, high-fiber diet
            - 🏃‍♀️ Walk, swim, cycle regularly
            - 🍽️ Avoid junk food and soda
            - 🧠 Track meals using an app
            - 👨‍⚕️ Visit a doctor or dietitian for guidance
            """)

        # --- BMI Comparison Chart ---
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

# Page: Endurance Estimator
elif page == "🧬 Endurance Estimator":
    st.title("🧬 Endurance Estimator")
    st.markdown("Estimate your endurance by answering a few questions:")
    q1 = st.slider("How long can you jog without stopping? (mins)", 1, 60, 10)
    q2 = st.slider("How many pushups can you do in one set?", 1, 100, 20)
    q3 = st.slider("How often do you exercise weekly?", 0, 7, 3)
    est = (q1/60)*0.4 + (q2/100)*0.3 + (q3/7)*0.3
    endurance_score = round(est * 10, 1)
    st.success(f"Estimated Endurance Score: **{endurance_score}/10**")

# Page: Aggression Scale
elif page == "💢 Aggression Scale":
    st.title("💢 Aggression Assessment")
    q1 = st.slider("How often do you get angry easily?", 1, 10, 5)
    q2 = st.slider("How likely are you to confront someone when annoyed?", 1, 10, 5)
    q3 = st.slider("Do you enjoy competitive environments?", 1, 10, 5)
    aggression_score = round((q1 + q2 + q3) / 3, 1)
    st.success(f"Your Aggression Score: **{aggression_score}/10**")

# Page: Diet Planner
elif page == "🥗 Diet Planner":
    st.title("🥗 Custom Diet Planner")
    weight = st.number_input("Current Weight (kg)", 30, 200, 70)
    target = st.number_input("Target Weight (kg)", 30, 200, 65)
    preference = st.selectbox("Diet Type", ["Balanced", "High Protein", "Vegetarian", "Low Carb"])

    if st.button("Generate Plan"):
        st.info("Generating personalized meal plan...")
        time.sleep(2)
        if target < weight:
            goal = "lose"
        elif target > weight:
            goal = "gain"
        else:
            goal = "maintain"

        st.success(f"Based on your goal to **{goal} weight**, here is a suggested {preference.lower()} plan:")
        if preference == "Balanced":
            st.markdown("""
            - 🥣 Breakfast: Oatmeal + banana + eggs
            - 🥗 Lunch: Brown rice + grilled chicken + vegetables
            - 🍽️ Dinner: Chapati + paneer + salad
            - 🍎 Snacks: Fruits, yogurt
            """)
        elif preference == "High Protein":
            st.markdown("""
            - 🍳 Breakfast: Eggs + nuts + protein shake
            - 🍛 Lunch: Quinoa + grilled tofu + lentils
            - 🥩 Dinner: Chicken breast + sweet potato + veggies
            - 🥜 Snacks: Greek yogurt, almonds
            """)
        elif preference == "Vegetarian":
            st.markdown("""
            - 🍞 Breakfast: Whole grain toast + avocado
            - 🍛 Lunch: Veg pulao + raita + salad
            - 🍲 Dinner: Dal + chapati + mixed veggies
            - 🥛 Snacks: Buttermilk, fruits
            """)
        else:
            st.markdown("""
            - 🍳 Breakfast: Eggs + avocado
            - 🥗 Lunch: Grilled chicken/fish + greens
            - 🥘 Dinner: Paneer + sauteed spinach
            - 🥜 Snacks: Nuts, cheese
            """)

        st.markdown("📥 To get this plan as a PDF or email export, please log in (optional). Coming soon!")
