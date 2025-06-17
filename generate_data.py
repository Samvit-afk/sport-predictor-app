import pandas as pd
import random

sports = [
    "Basketball", "Football", "Cricket", "Tennis", "Swimming", "Running",
    "Wrestling", "Boxing", "Badminton", "Volleyball", "Cycling", "Gymnastics",
    "Rowing", "Shooting", "Skiing", "Skateboarding", "Surfing", "Golf",
    "Rugby", "Karate", "Hockey", "Baseball", "Table Tennis", "Fencing"
]

def generate_sample():
    return {
        "Height_cm": random.randint(140, 210),
        "Weight_kg": random.randint(40, 120),
        "Age": random.randint(10, 40),
        "Strength": random.randint(1, 10),
        "Stamina": random.randint(1, 10),
        "Flexibility": random.randint(1, 10),
        "Speed": random.randint(1, 10),
        "Aggression": random.randint(1, 10),
        "Endurance": random.randint(1, 10),
        "Team_Player": random.choice([0, 1]),
        "Recommended_Sport": random.choice(sports)
    }

data = [generate_sample() for _ in range(100)]
df = pd.DataFrame(data)
df.to_csv("data.csv", index=False)

print("✅ Dataset created and saved as data.csv")
