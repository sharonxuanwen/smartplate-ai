
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Page config
st.set_page_config(page_title="SmartPlate AI", layout="centered")

# Title
st.title("🍽️ SmartPlate AI – Food Waste Insights & Prediction")
st.markdown("**Powered by: Plate Size & Food Waste Dataset**")
st.markdown("*Aligned with SDG 12: Responsible Consumption and Production*")

st.header("🔮 Predict Waste Based on Plate Size")
st.markdown("Enter your meal context below to estimate predicted food waste and receive portion tips.")

# Inputs
plate_size_cm = st.slider("Select Plate Size (cm)", min_value=25, max_value=35, value=30)
meal_type = st.selectbox("Meal Type", ["Breakfast", "Lunch", "Dinner"])
setting = st.selectbox("Dining Setting", ["Home", "Cafeteria", "Buffet"])

# ℹ️ Clarification note
st.caption("ℹ️ Note: In this prototype, plate sizes from the dataset are mapped as follows: 0 = Small (25 cm), 1 = Large (35 cm). "
           "The prediction tool uses plate size in centimeters to simulate practical application.")

# Simple prediction model (linear approximation)
predicted_waste = max(0, round(10 * (plate_size_cm - 25), 1))

# Output
st.subheader("📉 Predicted Waste")
st.metric(label="Estimated Waste (g)", value=f"{predicted_waste} g")

# Tips based on waste
st.subheader("💡 Smart Serving Tip")
if predicted_waste > 80:
    st.warning("Try reducing plate size to 27–28 cm to lower food waste.")
elif predicted_waste > 50:
    st.info("Moderate waste predicted. Consider portioning lighter.")
else:
    st.success("Efficient portion! Low predicted waste.")

st.divider()
st.subheader("📊 Upload Dataset for Full Analysis")

# Upload and visualize actual dataset
uploaded_file = st.file_uploader("Upload your plate-size dataset (.csv)", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    df['Waste (g)'] = df['g.served'] - df['g.consumed']
    df['Plate Label'] = df['plate size'].map({0: 'Small', 1: 'Large'})
    df['Plate Size (cm)'] = df['plate size'].map({0: 25, 1: 35})

    # Chart 1
    st.subheader("📊 Average Waste by Plate Size")
    waste_avg = df.groupby('Plate Label')['Waste (g)'].mean().reset_index()
    fig1, ax1 = plt.subplots()
    sns.barplot(x='Plate Label', y='Waste (g)', data=waste_avg, ax=ax1)
    ax1.set_title("Average Food Waste by Plate Size")
    st.pyplot(fig1)

    # Chart 2
    st.subheader("📊 Grams Served vs Consumed")
    served_vs_consumed = df.groupby('Plate Label')[['g.served', 'g.consumed']].mean().reset_index()
    df_melted = served_vs_consumed.melt(id_vars='Plate Label', value_vars=['g.served', 'g.consumed'])
    fig2, ax2 = plt.subplots()
    sns.barplot(x='Plate Label', y='value', hue='variable', data=df_melted, ax=ax2)
    ax2.set_title("Grams Served vs Consumed by Plate Size")
    st.pyplot(fig2)

    # Chart 3
    st.subheader("📉 Regression: Plate Size (cm) vs Waste")
    fig3, ax3 = plt.subplots()
    sns.regplot(x='Plate Size (cm)', y='Waste (g)', data=df, ci=None, scatter_kws={'s': 60}, ax=ax3)
    ax3.set_title("Regression: Plate Size (cm) vs Waste")
    ax3.set_xlabel("Plate Size (cm)")
    ax3.set_ylabel("Waste (g)")
    ax3.set_xlim(24, 36)
    st.pyplot(fig3)
else:
    st.info("Please upload the dataset to generate real-world insights.")
