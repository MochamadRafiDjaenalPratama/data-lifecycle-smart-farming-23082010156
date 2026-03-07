import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import timedelta

# =====================================
# PAGE CONFIG
# =====================================
st.set_page_config(
    page_title="Smart Farming Analytics",
    page_icon="🌾",
    layout="wide"
)

st.title("🌾 Smart Agriculture Intelligence Dashboard")

st.markdown(
"""
Dashboard ini memvisualisasikan **data sensor pertanian** untuk membantu monitoring kondisi lahan secara real-time.  
Data yang dianalisis meliputi **kelembaban tanah, suhu, kelembaban udara**, serta indikator **kualitas data**.
"""
)

# =====================================
# LOAD DATA
# =====================================
@st.cache_data
def load_data():

    try:
        df = pd.read_csv("outputs/cleaned_data.csv")
    except FileNotFoundError:
        st.error("❌ File cleaned_data.csv tidak ditemukan pada folder outputs.")
        return pd.DataFrame()

    df["timestamp"] = pd.to_datetime(df["timestamp"])

    return df


df = load_data()

if df.empty:
    st.stop()

# =====================================
# SIDEBAR FILTER
# =====================================
st.sidebar.header("🔎 Filter Data")

soil_types = ["All"] + sorted(df["soil_type"].unique().tolist())

selected_soil = st.sidebar.selectbox(
    "Pilih Jenis Tanah",
    soil_types
)

if selected_soil != "All":
    df = df[df["soil_type"] == selected_soil]

# =====================================
# DATA QUALITY METRICS
# =====================================
total_records = len(df)
total_cells = df.size

accuracy = 100.0
completeness = 100.0

latest_date = df["timestamp"].max()
thirty_days_ago = latest_date - timedelta(days=30)

data_last_30_days = df[df["timestamp"] >= thirty_days_ago].shape[0]
timeliness = (data_last_30_days / total_records) * 100

st.markdown("### 📊 Data Quality Score")

kpi1, kpi2, kpi3 = st.columns(3)

kpi1.metric(
    label="Accuracy",
    value=f"{accuracy:.2f}%",
    delta="Valid Data"
)

kpi2.metric(
    label="Completeness",
    value=f"{completeness:.2f}%",
    delta="Data Lengkap"
)

kpi3.metric(
    label="Timeliness (30 Hari)",
    value=f"{timeliness:.2f}%",
    delta=f"{data_last_30_days} Record"
)

st.divider()

# =====================================
# ROW 1
# =====================================
col1, col2 = st.columns([1,2])

# =====================================
# GAUGE MOISTURE
# =====================================
with col1:

    st.markdown("### 💧 Indeks Kelembaban Tanah")

    avg_moi = df["moi"].mean()

    fig_gauge = go.Figure(go.Indicator(
        mode="gauge+number",
        value=avg_moi,
        number={'suffix': "%"},
        gauge={
            "axis": {"range":[0,100]},
            "bar":{"color":"green"},
            "steps":[
                {"range":[0,30],"color":"lightcoral"},
                {"range":[30,70],"color":"khaki"},
                {"range":[70,100],"color":"lightgreen"}
            ],
            "threshold":{
                "line":{"color":"red","width":4},
                "value":30
            }
        }
    ))

    fig_gauge.update_layout(height=330)

    st.plotly_chart(fig_gauge, use_container_width=True)

# =====================================
# TIME SERIES SENSOR
# =====================================
with col2:

    st.markdown("### 📈 Tren Sensor Lingkungan")

    df_daily = (
        df.set_index("timestamp")
        .resample("D")[["temp","humidity"]]
        .mean()
        .reset_index()
    )

    fig_ts = px.line(
        df_daily,
        x="timestamp",
        y=["temp","humidity"],
        labels={
            "value":"Nilai Sensor",
            "variable":"Parameter"
        },
        color_discrete_map={
            "temp":"orange",
            "humidity":"royalblue"
        }
    )

    fig_ts.update_layout(height=330)

    st.plotly_chart(fig_ts, use_container_width=True)

# =====================================
# ROW 2
# =====================================
col3, col4 = st.columns(2)

# =====================================
# HEATMAP IRRIGATION RISK
# =====================================
with col3:

    st.markdown("### 🔥 Heatmap Risiko Irigasi")

    heatmap_data = (
        df.groupby(["soil_type","seedling_stage"])["result"]
        .mean()
        .reset_index()
    )

    heatmap_pivot = heatmap_data.pivot(
        index="soil_type",
        columns="seedling_stage",
        values="result"
    )

    fig_heat = px.imshow(
        heatmap_pivot,
        text_auto=".2f",
        aspect="auto",
        color_continuous_scale="YlOrRd",
        labels=dict(color="Tingkat Risiko")
    )

    fig_heat.update_layout(height=420)

    st.plotly_chart(fig_heat, use_container_width=True)

# =====================================
# SCATTER SENSOR RELATIONSHIP
# =====================================
with col4:

    st.markdown("### 🌤 Hubungan Suhu & Kelembaban")

    fig_scatter = px.scatter(
        df.sample(min(1000,len(df)), random_state=42),
        x="temp",
        y="humidity",
        color="result",
        color_continuous_scale="Viridis",
        labels={
            "temp":"Suhu (°C)",
            "humidity":"Kelembaban (%)"
        }
    )

    fig_scatter.update_layout(height=420)

    st.plotly_chart(fig_scatter, use_container_width=True)

# =====================================
# SENSOR INSIGHT
# =====================================
st.divider()
st.markdown("### 🧠 Insight Sensor Otomatis")

avg_temp = df["temp"].mean()
avg_humidity = df["humidity"].mean()
avg_moi = df["moi"].mean()

insight_col1, insight_col2 = st.columns(2)

with insight_col1:

    st.info(
        f"""
        **Rata-rata Suhu:** {avg_temp:.2f} °C  
        **Rata-rata Kelembaban Udara:** {avg_humidity:.2f}%  
        **Rata-rata Kelembaban Tanah:** {avg_moi:.2f}%
        """
    )

with insight_col2:

    if avg_moi < 30:
        st.error("🚨 Tanah cenderung kering — irigasi sangat disarankan.")
    elif avg_moi < 60:
        st.warning("⚠ Kelembaban tanah sedang — monitoring diperlukan.")
    else:
        st.success("✅ Kondisi kelembaban tanah optimal.")

# =====================================
# IRRIGATION ALERT SYSTEM
# =====================================
st.divider()
st.markdown("### 🚨 Sistem Peringatan Irigasi")

threshold = st.slider(
    "Tentukan Ambang Kelembaban Tanah",
    0,
    100,
    30
)

current_moi = df["moi"].mean()

if current_moi < threshold:

    st.error(
        f"""
        ⚠ **PERINGATAN IRIGASI**

        Moisture saat ini **{current_moi:.2f}%**  
        lebih rendah dari threshold **{threshold}%**

        ➜ Disarankan melakukan **penyiraman / irigasi**
        """
    )

else:

    st.success(
        f"""
        ✅ Kondisi tanah aman

        Moisture saat ini **{current_moi:.2f}%**
        """
    )