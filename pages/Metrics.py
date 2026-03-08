import streamlit as st
import pandas as pd
from utils.database import fetch_history
from utils.ui import apply_global_styles

st.set_page_config(
    page_title="Metrics & Statistics",
    page_icon="📊",
    layout="wide"
)

apply_global_styles()

st.markdown("<div class='main-card'>", unsafe_allow_html=True)

st.title("📊 Metrics & Statistics")
st.markdown("---")

data = fetch_history()

if not data:
    st.info("No data available yet. Run some detections first.")
    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# -------------------------------
# CREATE DATAFRAME
# -------------------------------
df = pd.DataFrame(
    data,
    columns=["Plate Number", "Confidence", "Timestamp"]
)

df["Timestamp"] = pd.to_datetime(df["Timestamp"])
df["Date"] = df["Timestamp"].dt.date

# -------------------------------
# KEY METRICS
# -------------------------------
total_detections = len(df)
avg_confidence = df["Confidence"].mean()
max_confidence = df["Confidence"].max()
min_confidence = df["Confidence"].min()

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Detections", total_detections)
col2.metric("Average Confidence", f"{avg_confidence:.2f}")
col3.metric("Highest Confidence", f"{max_confidence:.2f}")
col4.metric("Lowest Confidence", f"{min_confidence:.2f}")

st.markdown("---")

# -------------------------------
# DETECTIONS PER DAY (CHART)
# -------------------------------
st.subheader("📅 Detections Per Day")

daily_counts = df.groupby("Date").size().reset_index(name="Count")
st.bar_chart(daily_counts.set_index("Date"))

# -------------------------------
# MOST FREQUENT PLATES
# -------------------------------
st.subheader("🚗 Most Frequently Detected Plates")

top_plates = (
    df["Plate Number"]
    .value_counts()
    .head(5)
    .reset_index()
)
top_plates.columns = ["Plate Number", "Count"]

st.dataframe(top_plates, use_container_width=True)

st.markdown("</div>", unsafe_allow_html=True)
