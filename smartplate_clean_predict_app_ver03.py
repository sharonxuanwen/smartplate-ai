
import streamlit as st

# Page configuration
st.set_page_config(page_title="SmartPlate AI", layout="centered")

# Title and intro
st.title("🍽️ SmartPlate AI – Predict Food Waste")
st.markdown("**A simple tool to promote sustainable food choices**")
st.markdown("*Aligned with SDG 12: Responsible Consumption and Production*")

st.markdown("---")

# Input fields
st.header("🧾 Enter Meal Context")

plate_size_cm = st.slider("Select Plate Size (cm)", min_value=25, max_value=35, value=30)
meal_type = st.selectbox("Meal Type", ["Breakfast", "Lunch", "Dinner"])
setting = st.selectbox("Dining Setting", ["Home", "Cafeteria", "Buffet"])

st.caption("ℹ️ Plate size codes from the original dataset were 0 = Small (25 cm), 1 = Large (35 cm). "
           "This tool allows direct input in centimeters for better real-world simulation.")

# Prediction logic
predicted_waste = max(0, round(10 * (plate_size_cm - 25), 1))

st.markdown("---")

# Output section
st.header("📉 Predicted Waste")
st.metric(label="Estimated Waste (g)", value=f"{predicted_waste} g")

# Tips
st.subheader("💡 Smart Serving Tip")
if predicted_waste > 80:
    st.warning("Try reducing plate size to 27–28 cm to lower food waste.")
elif predicted_waste > 50:
    st.info("Moderate waste predicted. Consider portioning lighter.")
else:
    st.success("Efficient portion! Low predicted waste.")

st.markdown("---")
st.caption("Developed by Sharon Wong Xuan Wen | Data source: Plate Size Food Consumption Study – Kaggle")
