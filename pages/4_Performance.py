import streamlit as st
import pandas as pd
from utils.database import fetch_history
from utils.ui import apply_global_styles

st.set_page_config(
    page_title="Performance Evaluation",
    page_icon="📈",
    layout="wide"
)

apply_global_styles()

st.markdown("<div class='main-card'>", unsafe_allow_html=True)

st.title("📈 System Performance Evaluation")
st.markdown("---")

data = fetch_history()

if not data:
    st.info("No performance data available yet.")
    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

df = pd.DataFrame(
    data,
    columns=["Plate", "Confidence", "Timestamp", "Processing Time"]
)

# -------------------------------
# METRICS
# -------------------------------
total_attempts = len(df)
successful_detections = df["Plate"].notna().sum()
ocr_success = df[df["Plate"] != "Unreadable"].shape[0]

detection_rate = (successful_detections / total_attempts) * 100
ocr_success_rate = (ocr_success / total_attempts) * 100
avg_time = df["Processing Time"].mean()

col1, col2, col3 = st.columns(3)

col1.metric("Detection Success Rate", f"{detection_rate:.2f}%")
col2.metric("OCR Success Rate", f"{ocr_success_rate:.2f}%")
col3.metric("Avg Processing Time", f"{avg_time:.2f} sec")

st.markdown("---")

# -------------------------------
# TIME DISTRIBUTION
# -------------------------------
st.subheader("⏱️ Processing Time Distribution")
st.line_chart(df["Processing Time"])

st.markdown("</div>", unsafe_allow_html=True)
