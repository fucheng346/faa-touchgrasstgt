import os
import pandas as pd
from datetime import datetime

MOOD_FILE = "data/moods.csv"
CHALLENGE_FILE = "data/challenges.csv"

## create required data files if they dont exist
def init_files():
    if not os.path.exists("data"):
        os.makedirs("data")

    if not os.path.exists(MOOD_FILE):
        pd.DataFrame(columns = ["user_id", "date", "mood_score", "emotions", "reflection"]).to_csv(MOOD_FILE, index = False)

    if not os.path.exists(CHALLENGE_FILE):
        pd.DataFrame(columns = ["user_id", "date", "challenge", "completed"]).to_csv(CHALLENGE_FILE, index = False)


## save mood
def save_mood(user_id, mood_score, emotions, reflection):
    df = pd.read_csv(MOOD_FILE)
    new_entry = {"user_id": user_id, "date": datetime.today().strftime('%Y-%m-%d'),
                 "mood_score": mood_score, "emotions": ",".join(emotions), "reflection": reflection}

    df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index = True)
    df.to_csv(MOOD_FILE, index = False)

## save challenge
def save_challenge(user_id, challenge):
    df = pd.read_csv(CHALLENGE_FILE)
    new_entry = {"user_id": user_id, "date": datetime.today().strftime('%Y-%m-%d'), "challenge": challenge, "completed": True}

    df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index = True)
    df.to_csv(CHALLENGE_FILE, index = False)

# getters
def get_mood_data():
    return pd.read_csv(MOOD_FILE)

def get_challenge_data():
    return pd.read_csv(CHALLENGE_FILE)

# mood avg (by date)
def average_mood():
    df = get_mood_data()
    return df.groupby("date")["mood_score"].mean()

# freq of emotions
def emotion_freq():
    df = get_mood_data()
    emotions = []
    for entry in df["emotions"].dropna():
        emotions.extend(entry.split(","))
        
    return pd.Series(emotions).value_counts()

# percentage participation
def participation_perc():
    moods = get_mood_data()
    challenges = get_challenge_data()
    total_users = moods["user_id"].nunique()
    if total_users == 0:
        return 0
    
    challenge_users = challenges["user_id"].nunique()
    return challenge_users / total_users

# average mood change
def mood_improvement():
    df = get_mood_data()
    improvements = []
    for user in df["user_id"].unique():
        user_data = df[df["user_id"] == user].sort_values("date")
        if len(user_data) >= 2:
            diff = user_data["mood_score"].iloc[-1] - user_data["mood_score"].iloc[0]
            improvements.append(diff)

    if improvements:
        return sum(improvements) / len(improvements)
    return 0





