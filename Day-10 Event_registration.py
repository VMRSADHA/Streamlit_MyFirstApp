# event_app.py
import streamlit as st
import pandas as pd
from pathlib import Path

# --------------------
# Config
# --------------------
st.set_page_config(
    page_title="🎉 Event Registration App",
    page_icon="🎟️",
    layout="centered",
)

# CSS for styling (background + fonts)
page_bg = """
<style>
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
    color: black;
    font-family: "Comic Sans MS", cursive, sans-serif;
}
h1, h2, h3 {
    color: #ff5733;
    text-shadow: 1px 1px 2px #333333;
}
.stTextInput > div > div > input {
    background-color: #fff5e6;
    border: 2px solid #ff9f43;
    border-radius: 10px;
}
.stButton > button {
    background-color: #f368e0;
    color: white;
    border-radius: 12px;
    font-size: 18px;
    padding: 10px 20px;
}
.stButton > button:hover {
    background-color: #ee5253;
    color: yellow;
}
</style>
"""
st.markdown(page_bg, unsafe_allow_html=True)

# --------------------
# Header
# --------------------
st.title("🎉 Welcome to the Crazy Event Registration App 🕺💃")
st.subheader("Register now and let’s party like coders! 🖥️🍕")

# Funny GIFs
st.image("https://media.giphy.com/media/3oEjI6SIIHBdRxXI40/giphy.gif", caption="Get ready for the fun! 🎊", use_column_width=True)
st.image("https://media.giphy.com/media/l4FGuhL4U2WyjdkaY/giphy.gif", caption="Coding + Dancing = Perfect Combo 🕺", use_column_width=True)

# --------------------
# Registration Form
# --------------------
st.markdown("## ✍️ Fill in your details:")

events = ["🎤 Tech Talk", "🎮 Gaming Tournament", "🎵 Music Night", "🍕 Pizza Party", "🎬 Movie Marathon"]

name = st.text_input("👤 Your Name")
email = st.text_input("📧 Email Address")
event_choice = st.selectbox("🎯 Choose Your Event", events)
comments = st.text_area("💡 Any Special Requests?", placeholder="E.g., Need extra pizza 🍕🍕")

if "registrations.csv" not in st.session_state:
    st.session_state["registrations.csv"] = Path("registrations.csv")

# Submit button
if st.button("✅ Register Now"):
    if name.strip() == "" or email.strip() == "":
        st.error("⚠️ Please enter both name and email!")
    else:
        # Save to CSV
        file_path = st.session_state["registrations.csv"]
        if file_path.exists():
            df = pd.read_csv(file_path)
        else:
            df = pd.DataFrame(columns=["Name", "Email", "Event", "Comments"])

        new_entry = {"Name": name, "Email": email, "Event": event_choice, "Comments": comments}
        df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
        df.to_csv(file_path, index=False)

        st.success(f"🎉 Thanks {name}! You are registered for {event_choice} 🎟️")
        st.balloons()

# --------------------
# Show Registrations
# --------------------
st.markdown("---")
st.markdown("## 📋 Current Registrations:")

file_path = st.session_state["registrations.csv"]
if file_path.exists():
    df = pd.read_csv(file_path)
    st.dataframe(df.style.set_properties(**{'background-color': '#fff5e6',
                                            'color': 'black',
                                            'border-color': 'black'}))
else:
    st.info("No registrations yet. Be the first one! 🥳")
