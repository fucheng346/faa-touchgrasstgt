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
    mood = st.slider("How are you feeling today? :)", 1, 5)
    emotions = st.multiselect("Select emotions", EMOTIONS)
    reflection = st.text_area("Reflection (optional)")

    if st.button("Submit"):
        save_mood(st.session_state.user_id, mood, emotions, reflection)
        st.success("Mood saved!")

def page_daily_challenge():
    st.title("🔥 Today's Challenge")
    if "todays_challenge" not in st.session_state:
        st.session_state.todays_challenge = random.choice(CHALLENGES)
        
    st.write(st.session_state.todays_challenge)
    if st.button("Completed!"):
        if not st.session_state.completed_today:
            save_challenge(st.session_state.user_id, st.session_state.todays_challenge)
            st.success(f"Great job completing today's challenge! See you tomorrow :)")
            st.session_state.completed_today = True
            del st.session_state.todays_challenge
        else:
            st.warning(f"You have already completed today's challenge! See you tomorrow :)")

    # Post creation section
    st.markdown("---")
    st.subheader("🤝 Touch Grass Together - find friends to complete the challenge together!")
    time = st.time_input("Time")
    location = st.text_input("Location")

    if st.button("Post invite!"):
        make_invite(st.session_state.user_id, str(time), location)
        st.success("Invite posted!")

    st.markdown("### Make an Invite Today :)")

    # Join invite section
    invites = get_invites_today()
    if invites.empty:
        st.write("No invites created yet. Be the first!")
    else:
        for _, row in invites.iterrows():
            time = row["time"]
            loc = row["location"]
            participants = row["participants"].split(",")
            st.markdown(f"""
            <div style="border: 2px solid #4CAF50;
                border-radius: 10px;
                padding: 10px;
                margin-bottom: 10px;
                background-color: #f9f9f9;
            ">
            <b>🕒 {time} at {loc}</b><br>
            👥 {len(participants)} joined
            </div>
            """, unsafe_allow_html = True)
            
            if st.button("Join", key = row["post_id"]):
                join_invite(st.session_state.user_id, row["post_id"])
                st.success("You joined the invite!")



def page_community_dashboard():
    st.title("Community Insights")
    # Mood trend plot
    mood_trend = com_average_mood().reset_index()
    if (not mood_trend.empty):
        st.line_chart(mood_trend)
    else:
        st.write("No mood data yet...")

    # Emotion frequencies (bar chart)
    emotion_data = com_emotion_freq()
    if (not emotion_data.empty):
        st.bar_chart(emotion_data)
    else:
        st.write("No emotion data yet...")

    part_rate = round(com_participation_percentage() * 100, 2)
    mood_improve = round(com_mood_improvement(), 2)
    st.metric("Community Participation Rate", f"{part_rate}%")
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





