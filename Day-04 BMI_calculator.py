# app.py
import io
import datetime
import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd

# --- Utility functions ---
def calculate_bmi(weight_kg: float, height_cm: float) -> float:
    height_m = height_cm / 100.0
    if height_m <= 0:
        return 0.0
    return weight_kg / (height_m ** 2)

def bmi_category_and_emoji(bmi: float):
    if bmi <= 0:
        return ("Unknown", "❓")
    if bmi < 18.5:
        return ("Underweight", "🪶")
    if bmi < 25:
        return ("Normal weight", "✅")
    if bmi < 30:
        return ("Overweight", "⚠️")
    return ("Obese", "🚨")

# Initialize session state for history
if "history" not in st.session_state:
    st.session_state.history = []

# --- UI ---
st.set_page_config(page_title="BMI Calculator App", layout="centered")
st.title("⚖️ BMI Calculator App — Interactive")
st.write("Select gender, height and weight — see your BMI with a colorful chart and emoji!")

with st.sidebar:
    st.header("Options")
    unit = st.selectbox("Units", ["Metric (cm, kg)"], index=0)
    show_history = st.checkbox("Show calculation history", value=True)
    if st.button("Clear history"):
        st.session_state.history = []
        st.success("History cleared ✔️")

# Input area
col1, col2 = st.columns([1, 1])
with col1:
    gender = st.radio("Gender", ["Male", "Female", "Other"], index=0)
    height_cm = st.slider("Height (cm)", min_value=100, max_value=220, value=170)
with col2:
    weight_kg = st.number_input("Weight (kg)", min_value=10.0, max_value=300.0, value=70.0, step=0.1)
    compute = st.button("Calculate BMI")

# Compute and display
if compute:
    if height_cm <= 0 or weight_kg <= 0:
        st.error("Please enter valid positive height and weight.")
    else:
        bmi = round(calculate_bmi(weight_kg, height_cm), 2)
        category, emoji = bmi_category_and_emoji(bmi)
        st.metric(label="Your BMI", value=f"{bmi}", delta=f"{category} {emoji}")

        # Save to history
        st.session_state.history.append({
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "gender": gender,
            "height_cm": height_cm,
            "weight_kg": weight_kg,
            "bmi": bmi,
            "category": category
        })

        # --- Chart ---
        # Ranges for bars (start, end)
        ranges = [(0, 18.5), (18.5, 25), (25, 30), (30, 50)]
        labels = ["Underweight", "Normal", "Overweight", "Obese"]
        colors = ["#87CEEB", "#7CFC00", "#FFA500", "#FF4500"]

        fig, ax = plt.subplots(figsize=(8, 2.2))
        lefts = [r[0] for r in ranges]
        widths = [r[1]-r[0] for r in ranges]
        # draw stacked horizontal bars
        for left, width, color, label in zip(lefts, widths, colors, labels):
            ax.barh(0, width, left=left, color=color, alpha=0.9, height=0.6, edgecolor="k")

        # vertical line for user's BMI
        ax.axvline(x=bmi, color="black", linestyle="--", linewidth=2, label=f"Your BMI: {bmi}")
        ax.set_xlim(0, 50)
        ax.set_yticks([])
        ax.set_xlabel("BMI value")
        ax.set_title("BMI Categories 📊")
        ax.legend(loc="upper right")

        # annotate category near the BMI
        ax.text(bmi + 0.5, 0.1, f"{category} {emoji}", fontsize=12, fontweight="bold")

        st.pyplot(fig)

        # --- Download chart as PNG ---
        buf = io.BytesIO()
        fig.savefig(buf, format="png", bbox_inches="tight")
        buf.seek(0)
        st.download_button(
            label="⬇️ Download Chart (PNG)",
            data=buf,
            file_name="bmi_chart.png",
            mime="image/png"
        )

        # --- Download result as TXT ---
        result_text = (
            f"BMI Report\nTime: {datetime.datetime.now()}\n"
            f"Gender: {gender}\nHeight: {height_cm} cm\nWeight: {weight_kg} kg\n"
            f"BMI: {bmi}\nCategory: {category} {emoji}\n"
        )
        st.download_button(
            label="⬇️ Download Result (TXT)",
            data=result_text,
            file_name="bmi_result.txt",
            mime="text/plain"
        )

# Show history table & CSV download
if show_history and st.session_state.history:
    st.markdown("---")
    st.subheader("Calculation History ⏱️")
    df = pd.DataFrame(st.session_state.history)
    st.dataframe(df.sort_values("timestamp", ascending=False))

    csv_buf = df.to_csv(index=False).encode("utf-8")
    st.download_button("⬇️ Download History (CSV)", data=csv_buf, file_name="bmi_history.csv", mime="text/csv")
elif show_history:
    st.info("No history yet — calculate one or more BMIs to see entries here.")

st.caption("Made with ❤️ — try different heights/weights to see the marker move.")
