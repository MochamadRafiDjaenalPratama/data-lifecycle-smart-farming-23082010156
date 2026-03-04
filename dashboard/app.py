import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns
import matplotlib.pyplot as plt
from pathlib import Path

# ==============================
# Page Config
# ==============================
st.set_page_config(page_title="Smart Agriculture Dashboard", layout="wide")

st.title("🌾 Smart Agriculture Dashboard")

# ==============================
# Load Data (ROOT FOLDER)
# ==============================
data_path = Path("outputs/cleaned_data.csv")

if not data_path.exists():
    st.error("File cleaned_data.csv tidak ditemukan di root folder.")
    st.stop()

df = pd.read_csv(data_path)

# ==============================
# Sidebar Filter
# ==============================
st.sidebar.header("Filter Data")

soil_option = st.sidebar.selectbox(
    "Select Soil Type",
    df["Soil_Type"].unique()
)

filtered_df = df[df["Soil_Type"] == soil_option]

# ==============================
# Layout 2 Columns
# ==============================
col1, col2 = st.columns(2)

# ==============================
# 1️⃣ Scatter Plot
# ==============================
with col1:
    st.subheader("Moisture vs Temperature")

    fig1 = px.scatter(
        filtered_df,
        x="Soil_Moisture",
        y="Temperature_C",
        color="Crop_Result",
        title="Sensor Relationship"
    )

    st.plotly_chart(fig1, use_container_width=True)

# ==============================
# 2️⃣ Gauge Meter
# ==============================
with col2:
    st.subheader("Current Soil Moisture Level")

    current_moisture = filtered_df["Soil_Moisture"].mean()

    fig2 = go.Figure(go.Indicator(
        mode="gauge+number",
        value=current_moisture,
        title={'text': "Average Moisture"},
        gauge={
            'axis': {'range': [0, 100]},
            'bar': {'color': "blue"},
        }
    ))

    st.plotly_chart(fig2, use_container_width=True)

# ==============================
# 3️⃣ Correlation Heatmap
# ==============================
st.subheader("Sensor Correlation Heatmap")

corr = df[["Soil_Moisture", "Temperature_C", "Humidity_Percent"]].corr()

fig3, ax = plt.subplots()
sns.heatmap(corr, annot=True, cmap="coolwarm", ax=ax)
st.pyplot(fig3)

# ==============================
# 4️⃣ Alert System
# ==============================
st.subheader("Moisture Alert System")

threshold = st.slider("Set Moisture Threshold", 0, 100, 30)

if current_moisture < threshold:
    st.error("⚠ WARNING: Soil moisture below threshold!")
else:
    st.success("✅ Moisture level is safe.")

# ==============================
# 5️⃣ Soil Type Comparison
# ==============================
st.subheader("Average Sensor Values per Soil Type")

grouped = df.groupby("Soil_Type")[
    ["Soil_Moisture", "Temperature_C", "Humidity_Percent"]
].mean().reset_index()

fig5 = px.bar(
    grouped,
    x="Soil_Type",
    y=["Soil_Moisture", "Temperature_C", "Humidity_Percent"],
    barmode="group",
    title="Average Sensor Metrics"
)

st.plotly_chart(fig5, use_container_width=True)