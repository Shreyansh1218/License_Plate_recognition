import streamlit as st
from utils.ui import apply_global_styles

st.set_page_config(
    page_title="About",
    page_icon="ℹ️",
    layout="wide"
)

apply_global_styles()

st.markdown("<div class='main-card'>", unsafe_allow_html=True)

st.title("ℹ️ About This Project")

st.markdown("---")

st.markdown(
    """
    ### 🚗 License Plate Recognition System

    This project is an **AI-powered License Plate Recognition (LPR) system**
    built using **Deep Learning and Computer Vision**.

    It allows users to:
    - Upload or capture an image of a vehicle
    - Automatically detect the **license plate**
    - Extract the **plate number**
    - Display the **confidence score**
    - Store detection history for future reference

    ---
    ### 🧠 Technologies Used
    - **Python**
    - **Streamlit** – Web Interface
    - **YOLO (Ultralytics)** – License Plate Detection
    - **EasyOCR** – Text Recognition
    - **OpenCV** – Image Processing
    - **SQLite** – History Database

    ---
    ### 🎓 Project Purpose
    This project demonstrates the practical application of:
    - Computer Vision
    - Deep Learning
    - Real-time image analysis
    - End-to-end AI system design

    It is suitable for **academic submission, demonstrations, and further research**.

    ---
    """
)

st.markdown("</div>", unsafe_allow_html=True)
