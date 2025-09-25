# vmr_hotel_advanced.py
import streamlit as st
import pandas as pd
from pathlib import Path
from datetime import datetime, date
import urllib.parse

# --------------------
# CONFIG
# --------------------
st.set_page_config(page_title="VMR Hotel - Order & Billing", page_icon="🍽️", layout="wide")

DATA_DIR = Path("data")
ORDERS_FILE = DATA_DIR / "orders.csv"
DATA_DIR.mkdir(exist_ok=True, parents=True)

GST_RATE = 0.05  # 5%

# --------------------
# MENU
# --------------------
MENU = {
    "Breakfast": [
        {"id": "idly", "name": "Idly 🍚", "price": 30},
        {"id": "dosa", "name": "Dosa 🥞", "price": 50},
        {"id": "vada", "name": "Vada 🍩", "price": 25},
        {"id": "poori", "name": "Poori 🥯", "price": 40},
        {"id": "pongal", "name": "Pongal 🍲", "price": 45},
    ],
    "Beverages": [
        {"id": "coffee", "name": "Coffee ☕", "price": 20},
        {"id": "tea", "name": "Tea 🍵", "price": 15},
        {"id": "milk", "name": "Milk 🥛", "price": 10},
        {"id": "juice", "name": "Fruit Juice 🧃", "price": 35},
    ],
    "Desserts": [
        {"id": "payasam", "name": "Payasam 🍮", "price": 60},
        {"id": "icecream", "name": "Ice Cream 🍦", "price": 50},
        {"id": "gulab", "name": "Gulab Jamun 🍯", "price": 40},
    ]
}

# --------------------
# SESSION STATE
# --------------------
if "cart" not in st.session_state:
    st.session_state.cart = {}
if "last_order" not in st.session_state:
    st.session_state.last_order = None

def add_to_cart(item_id, qty):
    if qty > 0:
        st.session_state.cart[item_id] = st.session_state.cart.get(item_id, 0) + qty

def clear_cart():
    st.session_state.cart = {}

def save_order(order):
    df = pd.DataFrame([order])
    if ORDERS_FILE.exists():
        old = pd.read_csv(ORDERS_FILE)
        df = pd.concat([old, df], ignore_index=True)
    df.to_csv(ORDERS_FILE, index=False)

# --------------------
# HEADER
# --------------------
st.markdown(
    """
    <div style='background:linear-gradient(90deg,#34d399,#10b981);padding:20px;border-radius:10px;color:white;text-align:center'>
    <h1>🍽️ VMR Hotel — Order & Billing</h1>
    <p>Authentic & Tasty — Freshly served with ❤️</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# --------------------
# SELECT & ADD ITEMS
# --------------------
st.subheader("📋 Select Menu Items")
category = st.selectbox("Choose Category", list(MENU.keys()))
item = st.selectbox("Choose Item", [f"{m['name']} - ₹{m['price']}" for m in MENU[category]])
qty = st.number_input("Quantity", min_value=1, value=1, step=1)

if st.button("➕ Add to Cart"):
    item_id = [m for m in MENU[category] if f"{m['name']} - ₹{m['price']}" == item][0]["id"]
    add_to_cart(item_id, qty)
    st.success(f"Added {qty} x {item} to cart ✅")

# --------------------
# CART & BILL SUMMARY
# --------------------
st.subheader("🛒 Current Order")
cart = st.session_state.cart
if cart:
    rows, subtotal = [], 0
    for cat_items in MENU.values():
        for m in cat_items:
            if m["id"] in cart:
                qty = cart[m["id"]]
                total = qty * m["price"]
                subtotal += total
                rows.append([m["name"], qty, m["price"], total])
    df = pd.DataFrame(rows, columns=["Item", "Qty", "Rate (₹)", "Total (₹)"])
    st.table(df)

    gst = subtotal * GST_RATE
    total_amt = subtotal + gst
    st.write(f"**Subtotal: ₹{subtotal:.2f}**")
    st.write(f"GST (5%): ₹{gst:.2f}")
    st.write(f"### Grand Total: ₹{total_amt:.2f}")

    # WhatsApp share link
    msg = f"VMR Hotel Bill%0A------------------%0A"
    for r in rows:
        msg += f"{r[0]} x{r[1]} = ₹{r[3]}%0A"
    msg += f"Subtotal: ₹{subtotal:.2f}%0AGST: ₹{gst:.2f}%0ATotal: ₹{total_amt:.2f}"
    wa_url = f"https://wa.me/?text={urllib.parse.quote(msg)}"
    st.markdown(f"[📤 Share Bill on WhatsApp]({wa_url})", unsafe_allow_html=True)

    # Process order
    if st.button("✅ Process Order"):
        order = {
            "timestamp": datetime.now().isoformat(),
            "items": "; ".join([f"{r[0]} x{r[1]}" for r in rows]),
            "subtotal": subtotal,
            "gst": gst,
            "total": total_amt,
        }
        save_order(order)
        st.session_state.last_order = order
        clear_cart()
        st.success("Order processed successfully 🎉")

else:
    st.info("Cart is empty. Add items from menu above.")

# --------------------
# SALES ANALYTICS
# --------------------
st.subheader("📊 Sales Analytics")
if ORDERS_FILE.exists():
    df_orders = pd.read_csv(ORDERS_FILE)
    df_orders["timestamp"] = pd.to_datetime(df_orders["timestamp"])
    df_orders["date"] = df_orders["timestamp"].dt.date
    daily_sales = df_orders.groupby("date")["total"].sum()
    st.line_chart(daily_sales)
    st.bar_chart(daily_sales)
else:
    st.info("No sales data available yet.")
