import streamlit as st
import pandas as pd
from utils.database import fetch_history, clear_history
from utils.ui import apply_global_styles

st.set_page_config(
    page_title="Detection History",
    page_icon="📜",
    layout="wide"
)

apply_global_styles()

st.markdown("<div class='main-card'>", unsafe_allow_html=True)

st.title("📜 Detection History")
st.markdown("---")

# -------------------------------
# FETCH DATA
# -------------------------------
data = fetch_history()

if data:
    # Handle case where database returns 4 columns (ID included)
    if len(data[0]) == 4:
        df = pd.DataFrame(
            data,
            columns=["ID", "Plate Number", "Confidence", "Timestamp"]
        )
        df = df.drop(columns=["ID"])
    else:
        df = pd.DataFrame(
            data,
            columns=["Plate Number", "Confidence", "Timestamp"]
        )

    # -------------------------------
    # ACTION BUTTONS
    # -------------------------------
    col1, col2, col3 = st.columns([1, 1, 4])

    with col1:
        if st.button("🗑️ Clear History"):
            st.session_state.confirm_clear = True

    with col2:
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="📤 Export CSV",
            data=csv,
            file_name="license_plate_history.csv",
            mime="text/csv"
        )

    # -------------------------------
    # CONFIRM CLEAR
    # -------------------------------
    if st.session_state.get("confirm_clear", False):
        st.warning("⚠️ Are you sure you want to delete all history?")
        c1, c2 = st.columns(2)

        with c1:
            if st.button("✅ Yes, Clear"):
                clear_history()
                st.success("History cleared successfully.")
                st.session_state.confirm_clear = False
                st.rerun()

        with c2:
            if st.button("❌ Cancel"):
                st.session_state.confirm_clear = False

    st.markdown("---")

    # -------------------------------
    # TABLE
    # -------------------------------
    st.dataframe(df, use_container_width=True)

else:
    st.info("No detection history available yet.")

st.markdown("</div>", unsafe_allow_html=True)
