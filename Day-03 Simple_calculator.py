import streamlit as st

st.title("🧮 Simple Calculator")

# Take two numbers
num1 = st.number_input("Enter first number", value=0.0)
num2 = st.number_input("Enter second number", value=0.0)

# Select operation
operation = st.selectbox(
    "Select Operation",
    ("Add", "Subtract", "Multiply", "Divide")
)

# Button to calculate
if st.button("Calculate"):
    if operation == "Add":
        result = num1 + num2
        st.success(f"Result: {num1} + {num2} = {result}")
    elif operation == "Subtract":
        result = num1 - num2
        st.success(f"Result: {num1} - {num2} = {result}")
    elif operation == "Multiply":
        result = num1 * num2
        st.success(f"Result: {num1} × {num2} = {result}")
    elif operation == "Divide":
        if num2 == 0:
            st.error("Error: Division by zero is not allowed!")
        else:
            result = num1 / num2
            st.success(f"Result: {num1} ÷ {num2} = {result}")
