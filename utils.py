import os
import pandas as pd
from datetime import datetime
import uuid

MOOD_DATA = "data/moods.csv"
CHALLENGE_DATA = "data/challenges.csv"
GROUP_INVITES_DATA = "data/group_invites.csv"

## initialise files
def init_files():
    if not os.path.exists("data"):
        os.makedirs("data")

    if not os.path.exists(MOOD_DATA):
        pd.DataFrame(columns = ["user_id", "date", "mood_score", "emotions", "reflection"]).to_csv(MOOD_DATA, index = False)

    if not os.path.exists(CHALLENGE_DATA):
        pd.DataFrame(columns = ["user_id", "date", "challenge", "completed"]).to_csv(CHALLENGE_DATA, index = False)

    if not os.path.exists(GROUP_INVITES_DATA):
        pd.DataFrame(columns = ["post_id", "challenge_date", "inviter_id", "time", "location", "participants"]).to_csv(GROUP_INVITES_DATA, index = False)

## violating tell dont ask
def get_mood_data():
    return pd.read_csv(MOOD_DATA)

def get_challenge_data():
    return pd.read_csv(CHALLENGE_DATA)

def get_invites_today():
    try:
        df = pd.read_csv(GROUP_INVITES_DATA)
    except FileNotFoundError:
        return pd.DataFrame(columns=["post_id","challenge_date","inviter_id","time","location","participants"])
    today = datetime.today().strftime('%Y-%m-%d')
    return df[df["challenge_date"] == today]


## add user entry (mood, challenge, invite creation and invite joining)
def save_entry(file, new_entry): # general save entry function
    df = pd.DataFrame([new_entry])
    df.to_csv(file, mode = "a", header = False, index = False) 
        
def save_mood(user_id, mood_score, emotions, reflection): 
    new_entry = {"user_id": user_id, "date": datetime.today().strftime('%Y-%m-%d'),
                 "mood_score": mood_score, "emotions": ",".join(emotions), "reflection": reflection}
    save_entry(MOOD_DATA, new_entry)
    
def save_challenge(user_id, challenge):
    date = datetime.today().strftime('%Y-%m-%d')
    new_entry = {"user_id": user_id, "date": date, "challenge": challenge, "completed": True}
    save_entry(CHALLENGE_DATA, new_entry)


def make_invite(user_id, time, location):
    post_id = str(uuid.uuid4())
    date = datetime.today().strftime('%Y-%m-%d')
    new_entry = {"post_id": post_id, "challenge_date": date, "inviter_id": user_id, "time": time, "location": location, "participants": user_id}
    save_entry(GROUP_INVITES_DATA, new_entry)

def join_invite(user_id, post_id):
    df = pd.read_csv(GROUP_INVITES_DATA)
    row = df[df["post_id"] == post_id]
    if not row.empty:
        participants = row.iloc[0]["participants"].split(",")
        if user_id not in participants:
            participants.append(user_id)
            df.loc[df["post_id"] == post_id, "participants"] = ",".join(participants)
            df.to_csv(GROUP_INVITES_DATA, index = False)


## for community insights page
# community mood avg (by date)
def com_average_mood():
    df = get_mood_data().groupby("date")["mood_score"]
    return df.mean().reset_index()

# community emotion frequencies
def com_emotion_freq():
    df = (get_mood_data())["emotions"].dropna()
    emotions = []
    for entry in df:
        emotions.extend(entry.split(","))
    return pd.Series(emotions).value_counts()

# community percentage participation
def com_participation_percentage():
    moods = get_mood_data()
    challenges = get_challenge_data()
    total_users = moods["user_id"].nunique()
    if total_users == 0:
        return 0
    
    challenge_users = challenges["user_id"].nunique()
    return challenge_users / total_users

# community average mood change
def com_mood_improvement():
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





