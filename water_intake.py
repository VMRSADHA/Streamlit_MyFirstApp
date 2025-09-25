# app.py
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
from datetime import date, datetime, timedelta
from pathlib import Path
import csv
import uuid

# ---------------- Config ----------------
DATA_DIR = Path("data")
DATA_FILE = DATA_DIR / "water_liters.csv"
DAILY_GOAL_LITERS = 2.0  # default daily goal (2 liters)

# ---------------- Helpers ----------------
def ensure_data_file():
    DATA_DIR.mkdir(exist_ok=True)
    if not DATA_FILE.exists():
        with DATA_FILE.open("w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["id", "date", "liters"])

def load_data() -> pd.DataFrame:
    ensure_data_file()
    df = pd.read_csv(DATA_FILE)
    if df.empty:
        return pd.DataFrame(columns=["id", "date", "liters"])
    df["liters"] = pd.to_numeric(df["liters"], errors="coerce").fillna(0)
    return df

def save_data(df: pd.DataFrame):
    df.to_csv(DATA_FILE, index=False)

def add_entry(liters: float):
    df = load_data()
    new = {
        "id": str(uuid.uuid4()),
        "date": date.today().isoformat(),
        "liters": round(float(liters), 2),
    }
    df = pd.concat([df, pd.DataFrame([new])], ignore_index=True)
    save_data(df)

def get_summary(period="day"):
    """Return daily or weekly totals for the last 30 days."""
    df = load_data()
    if df.empty:
        return pd.Series(dtype=float)
    df["date"] = pd.to_datetime(df["date"])
    # last 30 days
    start = date.today() - timedelta(days=30)
    df = df[df["date"].dt.date >= start]

    if period == "week":
        grouped = df.groupby(df["date"].dt.isocalendar().week)["liters"].sum()
        grouped.index = [f"Week {i}" for i in grouped.index]
        return grouped
    else:
        return df.groupby(df["date"].dt.date)["liters"].sum()

# ---------------- Streamlit UI ----------------
st.set_page_config(page_title="Water Intake in Liters", layout="centered")
st.title("💧 Water Intake Tracker (Liters)")

# Input form
st.subheader("Add today's water intake")
liters = st.number_input("Liters", min_value=0.1, step=0.1, value=0.5)
if st.button("➕ Add Entry"):
    add_entry(liters)
    st.success(f"Added {liters} L for today.")

# Choose view type
st.markdown("---")
st.subheader("📊 Water Intake Graph")
view_type = st.radio("View by:", ["Day-by-Day", "Week-by-Week"])

if view_type == "Day-by-Day":
    series = get_summary("day")
else:
    series = get_summary("week")

if series.empty:
    st.info("No data yet. Add some water intake above ☝️")
else:
    # Plot with colored background
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.bar(series.index.astype(str), series.values, color="skyblue", edgecolor="black")

    # Add colored background
    ax.set_facecolor("#f0f8ff")  # light blue background
    fig.patch.set_facecolor("#e6f7ff")  # page background
    ax.set_title(f"Water Intake ({view_type}) - Last 30 Days", fontsize=14)
    ax.set_ylabel("Liters")
    plt.xticks(rotation=45)

    st.pyplot(fig)

# Show raw data
st.markdown("---")
st.subheader("📋 Raw Data")
df = load_data()
st.dataframe(df)
