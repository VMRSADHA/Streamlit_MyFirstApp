# app.py
import requests
import streamlit as st
import pandas as pd
from datetime import date, timedelta
from dotenv import load_dotenv

load_dotenv()

API_BASE = "https://api.exchangerate.host"
FALLBACK_PROVIDER = "https://api.frankfurter.app"
DEFAULT_FROM = "USD"
DEFAULT_TO = "EUR"

# ---------------------------
# Streamlit Page Config
# ---------------------------
st.set_page_config(page_title="Universal Currency Converter", layout="centered")

# ---------------------------
# Custom Styling
# ---------------------------
st.markdown(
    """
    <style>
    .stApp {
        background-color: #32CD32;   /* bright green */
        color: black;
    }
    h1, h2, h3, h4, h5, h6, p, div, span, label {
        color: black !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ---------------------------
# Title + Fun Emojis + GIF
# ---------------------------
st.markdown("## 💱💹💵 Universal Currency Converter 💶💴💷")
st.image(
    "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExNDM4b3VhdHZvYnpkdzRyOGoybnBkbWF6YTVkNzVxaDRrYTVvb2k1biZlcD12MV9naWZzX3NlYXJjaCZjdD1n/NFA61GS9qKZ68/giphy.gif",
    caption="💸 Real-time exchange rates in action!",
    use_column_width=True
)

st.markdown(
    "Easily convert between currencies, view 📈 historical charts, and download results. "
    "Powered by exchangerate.host (fallback: Frankfurter)."
)

# ---------------------------
# Debug toggle
# ---------------------------
show_debug = st.checkbox("Show debug output", value=False)

# ---------------------------
# API Helpers
# ---------------------------
@st.cache_data(ttl=3600)
def get_symbols():
    try:
        r = requests.get(f"{API_BASE}/symbols", timeout=8)
        r.raise_for_status()
        data = r.json()
        if data.get("symbols"):
            return data["symbols"]
    except Exception:
        pass
    # fallback
    return {
        "USD": {"description": "United States Dollar"},
        "EUR": {"description": "Euro"},
        "GBP": {"description": "British Pound"},
        "INR": {"description": "Indian Rupee"},
        "JPY": {"description": "Japanese Yen"},
        "AUD": {"description": "Australian Dollar"},
        "CAD": {"description": "Canadian Dollar"},
        "CNY": {"description": "Chinese Yuan"}
    }

def convert_amount(amount: float, from_curr: str, to_curr: str, conv_date: str = None):
    from_curr = (from_curr or "").upper()
    to_curr = (to_curr or "").upper()

    # same currency quick return
    if from_curr == to_curr:
        used_date = conv_date if conv_date else date.today().isoformat()
        return {"success": True, "provider": "same-currency",
                "query": {"from": from_curr, "to": to_curr, "amount": amount},
                "info": {"rate": 1.0}, "date": used_date, "result": float(amount)}

    # exchangerate.host
    try:
        params = {"from": from_curr, "to": to_curr, "amount": amount}
        if conv_date:
            params["date"] = conv_date
        r = requests.get(f"{API_BASE}/convert", params=params, timeout=10)
        r.raise_for_status()
        j = r.json()
        rate = j.get("info", {}).get("rate")
        result = j.get("result")
        if show_debug:
            st.write("DEBUG exchangerate.host response:", j)
        if rate is not None and result is not None:
            j["provider"] = "exchangerate.host"
            j["success"] = True
            return j
    except Exception as e:
        if show_debug:
            st.write("DEBUG exchangerate.host error:", repr(e))

    # fallback frankfurter
    try:
        if conv_date:
            url = f"{FALLBACK_PROVIDER}/{conv_date}"
        else:
            url = f"{FALLBACK_PROVIDER}/latest"
        params_f = {"amount": amount, "from": from_curr, "to": to_curr}
        r2 = requests.get(url, params=params_f, timeout=10)
        r2.raise_for_status()
        j2 = r2.json()
        if show_debug:
            st.write("DEBUG frankfurter response:", j2)
        rates = j2.get("rates", {})
        rate_val = rates.get(to_curr)
        if rate_val is not None:
            result_val = float(amount) * float(rate_val)
            return {"success": True, "provider": "frankfurter",
                    "query": {"from": from_curr, "to": to_curr, "amount": amount},
                    "info": {"rate": float(rate_val)}, "date": j2.get("date"), "result": result_val}
    except Exception as e:
        if show_debug:
            st.write("DEBUG frankfurter error:", repr(e))

    return {"success": False, "provider": None}

@st.cache_data(ttl=600)
def fetch_timeseries(from_curr: str, to_curr: str, start_date: str, end_date: str):
    params = {"start_date": start_date, "end_date": end_date, "base": from_curr, "symbols": to_curr}
    r = requests.get(f"{API_BASE}/timeseries", params=params, timeout=15)
    r.raise_for_status()
    data = r.json()
    if not data.get("rates"):
        raise RuntimeError("No rates in response")
    items = []
    for d, entry in sorted(data["rates"].items()):
        rate = entry.get(to_curr)
        items.append((d, rate))
    df = pd.DataFrame(items, columns=["date", "rate"])
    df["date"] = pd.to_datetime(df["date"])
    df.set_index("date", inplace=True)
    return df["rate"]

# ---------------------------
# UI
# ---------------------------
symbols = get_symbols()
codes = sorted(symbols.keys())

col1, col2 = st.columns([1,1])
with col1:
    amount = st.number_input("💵 Amount", value=1.0, format="%.2f")
    from_curr = st.selectbox("From Currency 💲", codes, index=codes.index(DEFAULT_FROM) if DEFAULT_FROM in codes else 0)
with col2:
    to_curr = st.selectbox("To Currency 💱", codes, index=codes.index(DEFAULT_TO) if DEFAULT_TO in codes else 1)
    if st.button("🔄 Swap"):
        from_curr, to_curr = to_curr, from_curr
        st.experimental_rerun()

conv_date = None
if st.checkbox("📅 Use specific date for conversion (historical)?", value=False):
    conv_date = st.date_input("Conversion date", value=date.today() - timedelta(days=1)).isoformat()

if st.button("🚀 Convert"):
    resp = convert_amount(amount, from_curr, to_curr, conv_date)
    if not resp.get("success"):
        st.error("❌ Could not fetch a valid exchange rate. Try again later or with different currencies.")
    else:
        rate = resp.get("info", {}).get("rate")
        result = resp.get("result")
        used_date = resp.get("date")
        provider = resp.get("provider")
        st.metric(label=f"{amount} {from_curr} → {to_curr} ({provider})", value=f"{result:,.2f}")
        st.write(f"💹 Exchange rate: 1 {from_curr} = {rate:,.6f} {to_curr}  (date: {used_date})")
        if rate:
            st.write(f"📊 Inverse: 1 {to_curr} = {1/rate:,.6f} {from_curr}")

        # download
        summary = f"Conversion result\nProvider: {provider}\nDate: {used_date}\n{amount} {from_curr} = {result:,.2f} {to_curr}\nRate: {rate}"
        st.download_button("⬇️ Download result (TXT)", data=summary, file_name="conversion.txt", mime="text/plain")

st.markdown("---")
st.subheader("📈 Historical rates (time series)")

days = st.slider("Days back to show", 7, 365, 90)
end_dt = date.today()
start_dt = end_dt - timedelta(days=days)
if st.button("📊 Show historical chart"):
    try:
        series = fetch_timeseries(from_curr, to_curr, start_dt.isoformat(), end_dt.isoformat())
        st.line_chart(series)
        csv = series.reset_index().to_csv(index=False).encode("utf-8")
        st.download_button("⬇️ Download rates CSV", data=csv, file_name="rates.csv", mime="text/csv")
    except Exception as e:
        st.error(f"⚠️ Could not fetch timeseries: {e}")

st.markdown("---")
st.caption("💼 Powered by exchangerate.host (fallback: Frankfurter).")
