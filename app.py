import streamlit as st
import uuid
from utils import init_files


# Initialize required files
init_files()


# Create a unique user ID per session
if "user_id" not in st.session_state:
    st.session_state.user_id = str(uuid.uuid4())


# Sidebar navigation
page = st.sidebar.selectbox(
    "Navigate",
    ["Log Mood", "Daily Challenge", "Community Dashboard"]
)


# Page content
if page == "Log Mood":
    st.title("🌤️ Mood Logger")
    mood = st.text_input("How are you feeling today?")
    if st.button("Save Mood"):
        st.success(f"Mood saved: {mood}")

elif page == "Daily Challenge":
    st.title("🔥 Daily Challenge")
    st.write("Take a 10-minute walk today.")

elif page == "Community Dashboard":
    st.title("🌍 Community Dashboard")
    st.write("Community stats coming soon...")
