# app.py
import streamlit as st
import random
import csv
from pathlib import Path
from datetime import datetime
import pandas as pd
import time

# ---------------------
# Config
# ---------------------
DATA_DIR = Path("data")
SCORES_FILE = DATA_DIR / "scores.csv"
NUM_QUESTIONS_DEFAULT = 8

# Ensure data directory
DATA_DIR.mkdir(exist_ok=True)

# ---------------------
# Quiz questions (Nature & Curiosity)
# Add / edit questions here: 'question','choices'(list),'answer' (exact text), 'explain'
# ---------------------
QUESTIONS = [
    {
        "question": "🌲 What process do plants use to convert sunlight into chemical energy?",
        "choices": ["Respiration", "Photosynthesis", "Transpiration", "Fermentation"],
        "answer": "Photosynthesis",
        "explain": "Photosynthesis converts sunlight, CO₂ and water into glucose and oxygen in plant chloroplasts."
    },
    {
        "question": "🦋 Which stage is NOT part of a butterfly's life cycle?",
        "choices": ["Egg", "Pupa", "Nymph", "Adult"],
        "answer": "Nymph",
        "explain": "Butterflies undergo complete metamorphosis: egg → larva (caterpillar) → pupa → adult."
    },
    {
        "question": "🌍 Which layer of Earth is liquid and lies beneath the crust?",
        "choices": ["Inner core", "Mantle", "Outer core", "Lithosphere"],
        "answer": "Outer core",
        "explain": "The outer core is liquid iron and nickel; the inner core is solid."
    },
    {
        "question": "🔬 What is the smallest unit of life that can function independently?",
        "choices": ["Atom", "Molecule", "Cell", "Tissue"],
        "answer": "Cell",
        "explain": "The cell is the basic structural and functional unit of all living organisms."
    },
    {
        "question": "🌊 What causes ocean tides on Earth?",
        "choices": ["Wind patterns", "Earthquakes", "Gravitational pull of Moon and Sun", "Ocean currents"],
        "answer": "Gravitational pull of Moon and Sun",
        "explain": "Tides are primarily caused by the gravitational forces of the Moon and the Sun acting on Earth's oceans."
    },
    {
        "question": "🍄 Fungi get their nutrients by:",
        "choices": ["Photosynthesis", "Absorbing organic matter", "Ingesting bacteria", "Filtering water"],
        "answer": "Absorbing organic matter",
        "explain": "Fungi secrete enzymes to break down organic material and absorb nutrients."
    },
    {
        "question": "🦈 Sharks are classified as:",
        "choices": ["Bony fish", "Mammals", "Cartilaginous fish", "Birds"],
        "answer": "Cartilaginous fish",
        "explain": "Sharks have skeletons made of cartilage (not bone), so they are cartilaginous fishes."
    },
    {
        "question": "🌱 Which phenomenon is responsible for seeds being carried away by wind?",
        "choices": ["Pollination", "Seed dispersal", "Germination", "Photosynthesis"],
        "answer": "Seed dispersal",
        "explain": "Seed dispersal helps plants spread offspring; wind dispersal is a common method."
    },
    {
        "question": "☀️ The tilt of Earth's axis is responsible for:",
        "choices": ["Day and night", "Seasons", "Tides", "Volcanoes"],
        "answer": "Seasons",
        "explain": "Earth's axial tilt (≈23.5°) leads to varying sunlight angles across the year → seasons."
    },
    {
        "question": "🐝 Bees communicate primarily by:",
        "choices": ["Vocal sounds", "Dance language and pheromones", "Electrical signals", "Color flashes"],
        "answer": "Dance language and pheromones",
        "explain": "Bees use dance moves and chemical signals (pheromones) to convey location of food and other info."
    }
]

# ---------------------
# Helpers
# ---------------------
def init_session():
    if "shuffled_questions" not in st.session_state:
        st.session_state.shuffled_questions = []
    if "current_index" not in st.session_state:
        st.session_state.current_index = 0
    if "score" not in st.session_state:
        st.session_state.score = 0
    if "answers" not in st.session_state:
        st.session_state.answers = []
    if "start_time" not in st.session_state:
        st.session_state.start_time = None
    if "timed_mode" not in st.session_state:
        st.session_state.timed_mode = False
    if "time_per_question" not in st.session_state:
        st.session_state.time_per_question = 20  # seconds

def load_high_scores():
    if not SCORES_FILE.exists():
        return pd.DataFrame(columns=["name","score","total","date","time_taken_s"])
    try:
        return pd.read_csv(SCORES_FILE)
    except Exception:
        return pd.DataFrame(columns=["name","score","total","date","time_taken_s"])

def save_high_score(name, score, total, time_taken_s):
    df = load_high_scores()
    df = df.append({"name": name, "score": score, "total": total, "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "time_taken_s": time_taken_s}, ignore_index=True)
    df.to_csv(SCORES_FILE, index=False)

def start_quiz(num_questions: int, timed: bool, time_per_q: int):
    # choose questions randomly
    pool = QUESTIONS.copy()
    random.shuffle(pool)
    selected = pool[:num_questions]
    # shuffle choices for each
    for q in selected:
        choices = q["choices"].copy()
        random.shuffle(choices)
        q["_shuffled_choices"] = choices
    st.session_state.shuffled_questions = selected
    st.session_state.current_index = 0
    st.session_state.score = 0
    st.session_state.answers = []
    st.session_state.start_time = time.time()
    st.session_state.timed_mode = timed
    st.session_state.time_per_question = time_per_q

def answer_current(selected_choice):
    idx = st.session_state.current_index
    q = st.session_state.shuffled_questions[idx]
    correct = selected_choice == q["answer"]
    explain = q.get("explain","")
    st.session_state.answers.append({
        "question": q["question"],
        "selected": selected_choice,
        "correct": correct,
        "correct_answer": q["answer"],
        "explain": explain
    })
    if correct:
        st.session_state.score += 1
    st.session_state.current_index += 1

# ---------------------
# UI layout
# ---------------------
st.set_page_config(page_title="Nature & Curiosity Quiz 🌿", layout="centered")
st.title("Nature & Curiosity Quiz 🌿🧠")
st.write("Test your nature knowledge and satisfy your curiosity! ✅ Select mode and press Start.")

init_session()

# Sidebar / Settings
with st.sidebar:
    st.header("Quiz Settings")
    num_q = st.slider("Number of questions", min_value=3, max_value=min( len(QUESTIONS), 15), value=NUM_QUESTIONS_DEFAULT)
    timed = st.checkbox("Timed mode (per question)", value=False)
    time_per_q = st.slider("Seconds per question", min_value=5, max_value=60, value=20) if timed else 20
    if st.button("🔁 Start New Quiz"):
        start_quiz(num_q, timed, time_per_q)

    st.markdown("---")
    st.write("🏆 High Scores")
    hs = load_high_scores()
    if not hs.empty:
        st.dataframe(hs.sort_values(by=["score","date"], ascending=[False,False]).head(10))
    else:
        st.write("No scores yet. Be the first! 🎉")

# If no quiz started, show intro / start button
if not st.session_state.shuffled_questions:
    st.markdown("### How to play")
    st.write(
        "- Choose number of questions and whether you want Timed mode (each question will auto-submit when time runs out).\n"
        "- Click **Start New Quiz** in the left panel.\n"
        "- You will get instant feedback after each question and a final score at the end. Good luck! 🍀"
    )
    st.stop()

# Quiz in progress
total_q = len(st.session_state.shuffled_questions)
idx = st.session_state.current_index

# If finished
if idx >= total_q:
    total_time = int(time.time() - st.session_state.start_time) if st.session_state.start_time else 0
    st.success(f"Quiz completed! 🎉 Your score: {st.session_state.score} / {total_q}")
    name = st.text_input("Enter your name to save score (optional):")
    if st.button("💾 Save Score"):
        save_high_score(name if name else "Anonymous", st.session_state.score, total_q, total_time)
        st.success("Saved! Check High Scores in the left panel.")
    st.markdown("### Review")
    for a in st.session_state.answers:
        color = "✅" if a["correct"] else "❌"
        st.write(f"{color} **Q:** {a['question']}")
        st.write(f"Your answer: **{a['selected']}** — Correct answer: **{a['correct_answer']}**")
        if a["explain"]:
            st.info(a["explain"])
    if st.button("↻ Play Again"):
        start_quiz(num_q, timed, time_per_q)
    st.stop()

# Show current question
q = st.session_state.shuffled_questions[idx]
st.markdown(f"**Question {idx+1} / {total_q}**")
st.write(q["question"])

# Timer (if timed_mode)
if st.session_state.timed_mode:
    remaining = st.session_state.time_per_question
    # Compute how many seconds have passed for this question (naive)
    # We store question start in session_state ideally, but simple countdown per render:
    if f"start_q_{idx}" not in st.session_state:
        st.session_state[f"start_q_{idx}"] = time.time()
    elapsed = int(time.time() - st.session_state[f"start_q_{idx}"])
    remaining = max(0, st.session_state.time_per_question - elapsed)
    st.progress((idx + (st.session_state.time_per_question - remaining)/st.session_state.time_per_question) / total_q)
    st.write(f"⏱️ Time left for this question: **{remaining}** seconds")
    if remaining == 0:
        # auto-submit with no selection => treat as wrong (or could pick None)
        answer_current(selected_choice="(No answer)")
        st.experimental_rerun()
else:
    st.progress(idx / total_q)

# Show choices
choices = q["_shuffled_choices"]
selected = st.radio("Choose one option:", choices, key=f"choice_{idx}")

col1, col2 = st.columns([1,1])
with col1:
    if st.button("✅ Submit Answer"):
        answer_current(selected_choice=selected)
        st.experimental_rerun()
with col2:
    if st.button("💡 Show Hint / Explanation"):
        if q.get("explain"):
            st.info(q["explain"])
        else:
            st.info("No hint available for this question.")

# Small footer & score
st.markdown("---")
st.write(f"Score: **{st.session_state.score}** / {total_q}  —  Question {idx+1}/{total_q}")
