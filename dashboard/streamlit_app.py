import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns
import matplotlib.pyplot as plt
from pathlib import Path
from datetime import datetime, timedelta

# ==============================
# Page Config
# ==============================
st.set_page_config(
    page_title="Dashboard Smart Farming",
    layout="wide",
    page_icon="🌾"
)

# ==============================
# Title
# ==============================
st.title("🌾 Dashboard Smart Farming IoT")
st.markdown("Monitoring sensor pertanian berbasis Data Lifecycle Management")

# ==============================
# Load Data
# ==============================
data_path = Path("outputs/cleaned_data.csv")

if not data_path.exists():
    st.error("File cleaned_data.csv tidak ditemukan.")
    st.stop()

df = pd.read_csv(data_path)

# Jika ada kolom waktu
if "Timestamp" in df.columns:
    df["Timestamp"] = pd.to_datetime(df["Timestamp"])

# ==============================
# ==============================
# 📊 DATA QUALITY SCORE
# ==============================
# ==============================

total_cells = df.size
missing_cells = df.isnull().sum().sum()
non_null_cells = total_cells - missing_cells

accuracy_score = 1 - (missing_cells / total_cells)
completeness_score = non_null_cells / total_cells

if "Timestamp" in df.columns:
    last_30_days = datetime.now() - timedelta(days=30)
    recent_data = df[df["Timestamp"] >= last_30_days]
    timeliness_score = len(recent_data) / len(df)
else:
    timeliness_score = 1.0  # jika tidak ada waktu, dianggap lengkap

st.markdown("## 📈 Data Quality Score")

col_m1, col_m2, col_m3 = st.columns(3)

col_m1.metric("🎯 Accuracy", f"{accuracy_score:.2%}")
col_m2.metric("📦 Completeness", f"{completeness_score:.2%}")
col_m3.metric("⏳ Timeliness", f"{timeliness_score:.2%}")

st.markdown("---")

# ==============================
# Sidebar Filter
# ==============================
st.sidebar.header("⚙️ Filter Data")

soil_option = st.sidebar.selectbox(
    "Pilih Jenis Tanah",
    df["Soil_Type"].unique()
)

filtered_df = df[df["Soil_Type"] == soil_option]

# ==============================
# 1️⃣ Time Series
# ==============================
st.subheader("📊 Tren Sensor dari Waktu ke Waktu")

if "Timestamp" in filtered_df.columns:
    fig_ts = px.line(
        filtered_df,
        x="Timestamp",
        y=["Soil_Moisture", "Temperature_C", "Humidity_Percent"],
        title="Tren Perubahan Sensor"
    )
    st.plotly_chart(fig_ts, use_container_width=True)
else:
    st.info("Kolom Timestamp tidak tersedia untuk time series.")

# ==============================
# Layout 2 Columns
# ==============================
col1, col2 = st.columns(2)

# ==============================
# 2️⃣ Gauge Meter
# ==============================
with col1:
    st.subheader("💧 Kelembaban Tanah Saat Ini")

    current_moisture = filtered_df["Soil_Moisture"].mean()

    fig_gauge = go.Figure(go.Indicator(
        mode="gauge+number",
        value=current_moisture,
        title={'text': "Rata-rata Kelembaban"},
        gauge={
            'axis': {'range': [0, 100]},
            'bar': {'color': "#2E86C1"},
            'steps': [
                {'range': [0, 30], 'color': "#E74C3C"},
                {'range': [30, 70], 'color': "#F4D03F"},
                {'range': [70, 100], 'color': "#27AE60"}
            ],
        }
    ))

    st.plotly_chart(fig_gauge, use_container_width=True)

# ==============================
# 3️⃣ Alert System
# ==============================
with col2:
    st.subheader("🚨 Sistem Peringatan Kelembaban")

    threshold = st.slider("Tentukan Ambang Batas", 0, 100, 30)

    if current_moisture < threshold:
        st.error("🔴 PERINGATAN: Kelembaban tanah di bawah ambang batas!")
    else:
        st.success("🟢 Kondisi kelembaban dalam batas aman.")

# ==============================
# 4️⃣ Correlation Heatmap
# ==============================
st.subheader("🔥 Heatmap Korelasi Antar Sensor")

sensor_cols = ["Soil_Moisture", "Temperature_C", "Humidity_Percent"]

corr = df[sensor_cols].corr()

fig_hm, ax = plt.subplots()
sns.heatmap(corr, annot=True, cmap="RdYlGn", ax=ax)
st.pyplot(fig_hm)

st.markdown("---")

# ==============================
# Additional Insight
# ==============================
st.subheader("📊 Rata-rata Sensor per Jenis Tanah")

grouped = df.groupby("Soil_Type")[sensor_cols].mean().reset_index()

fig_bar = px.bar(
    grouped,
    x="Soil_Type",
    y=sensor_cols,
    barmode="group",
    title="Perbandingan Rata-rata Sensor"
)

st.plotly_chart(fig_bar, use_container_width=True)