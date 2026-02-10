import streamlit as st
import random
import uuid
from utils import *

st.set_page_config(page_title="Touch Grass Together", layout="centered")

## Placeholders
EMOTIONS = ["Stressed", "Lonely", "Calm", "Happy", "Motivated", "Anxious"]
CHALLENGES = ["Take a 10-minute walk today.", ""] ##### angie come up with the challenges here and can also add some more emotions

# Create a unique user ID per session
if "user_id" not in st.session_state:
    st.session_state.user_id = str(uuid.uuid4())

# Initialize required files
init_files()

### Page functions
def page_log_mood():
    st.title("🌤 Mood Logger")
    mood = st.slider("How good are you feeling today? :)", 1, 5)
    emotions = st.multiselect("Select emotions", EMOTIONS)
    reflection = st.text_area("Reflection (optional)")

    if st.button("Submit"):
        save_mood(st.session_state.user_id, mood, emotions, reflection)
        st.success(f"Mood saved!")

def page_daily_challenge():
    st.title("🔥 Today's Challenge")

    if "todays_challenge" not in st.session_state:
        st.session_state.todays_challenge = random.choice(CHALLENGES)
        
    st.write(st.session_state.todays_challenge)
    if st.button("Completed!"):
        save_challenge(st.session_state.user_id, st.session_state.todays_challenge)
        st.success(f"Great job completing today's challenge! See you tomorrow :)")
        del st.session_state.todays_challenge

def page_community_dashboard():
    st.title("Community Insights")
    # Mood trend plot
    mood_trend = average_mood()
    if (not mood_trend.empty):
        st.line_chart(mood_trend)
    else:
        st.write("No mood data yet...")

    # Emotion frequencies (bar chart)
    emotion_data = emotion_freq()
    if (not emotion_data.empty):
        st.bar_chart(emotion_data)
    else:
        st.write("No emotion data yet...")

    part_rate = round(participation_perc() * 100, 2)
    mood_improve = round(mood_improvement(), 2)
    st.metric("Participation Rate", f"{part_rate}%")
    st.metric("Avg Mood Improvement", f"{mood_improve}")



# Sidebar navigation / page selection
page = st.sidebar.selectbox("Navigate", ["Log Mood", "Daily Challenge", "Community Dashboard"])


# Page routing
if page == "Log Mood":
    page_log_mood()

# Daily Challenge
elif page == "Daily Challenge":
    page_daily_challenge()

# Community Dashboard
elif page == "Community Dashboard":
    page_community_dashboard()





