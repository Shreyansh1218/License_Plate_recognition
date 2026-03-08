import streamlit as st
from PIL import Image
import io
import time

from utils.ui import apply_global_styles
from utils.detector import detect_license_plate
from utils.database import init_db, insert_record

# -------------------------------
# INIT DATABASE
# -------------------------------
init_db()

# -------------------------------
# PAGE CONFIG
# -------------------------------
st.set_page_config(
    page_title="License Plate Recognition",
    page_icon="🚗",
    layout="wide"
)

apply_global_styles()

# -------------------------------
# CONFIDENCE BADGE
# -------------------------------
def show_confidence_badge(confidence):
    if confidence >= 0.85:
        st.success(f"🟢 High Confidence Detection ({confidence:.2f})")
    elif confidence >= 0.65:
        st.warning(f"🟡 Medium Confidence Detection ({confidence:.2f})")
    else:
        st.error(f"🔴 Low Confidence Detection ({confidence:.2f})")

# -------------------------------
# MAIN UI
# -------------------------------
st.markdown("<div class='main-card'>", unsafe_allow_html=True)

st.title("🚗 License Plate Recognition System")
st.write("Upload or capture an image to detect the license plate")

st.markdown("---")

# -------------------------------
# INPUT METHOD
# -------------------------------
input_method = st.radio(
    "Choose input method",
    ["Upload Image", "Use Camera"]
)

image = None

# -------------------------------
# IMAGE INPUT
# -------------------------------
if input_method == "Upload Image":
    uploaded_file = st.file_uploader(
        "Upload vehicle image",
        type=["jpg", "jpeg", "png", "jfif"]
    )
    if uploaded_file:
        image = Image.open(uploaded_file).convert("RGB")

else:
    camera_image = st.camera_input("Capture image", key="camera")

    if camera_image:
        image = Image.open(io.BytesIO(camera_image.getvalue())).convert("RGB")

        # Clear photo button (safe reset)
        if st.button("❌ Clear photo"):
            st.rerun()

# -------------------------------
# PREVIEW & DETECTION
# -------------------------------
if image:
    # INPUT IMAGE (CONTROLLED SIZE)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image(
            image,
            caption="Input Image",
            width=450
        )

    st.markdown("---")

    if st.button("🔍 Detect License Plate"):
        with st.spinner("Detecting license plate..."):
            start_time = time.time()

            annotated_img, plate_text, confidence = detect_license_plate(image)

            processing_time = time.time() - start_time

        # OUTPUT IMAGE (CONTROLLED SIZE)
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.image(
                annotated_img,
                caption="Detected License Plate",
                width=550
            )

        # RESULTS
        if plate_text and confidence:
            st.success(f"Plate Number: {plate_text}")

            show_confidence_badge(confidence)

            st.info(f"Processing Time: {processing_time:.2f} seconds")

            insert_record(plate_text, confidence, processing_time)
        else:
            st.warning("No license plate detected. Try a clearer image.")

st.markdown("</div>", unsafe_allow_html=True)