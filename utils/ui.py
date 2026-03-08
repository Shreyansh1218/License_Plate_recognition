import streamlit as st

def apply_global_styles():
    st.markdown(
        """
        <style>
        /* Full page background */
        .stApp {
            background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
            color: #ffffff;
        }

        /* Centered card */
        .main-card {
            background: rgba(255, 255, 255, 0.08);
            padding: 2rem;
            border-radius: 16px;
            max-width: 900px;
            margin: auto;
            box-shadow: 0 8px 32px rgba(0,0,0,0.3);
        }

        /* Buttons */
        .stButton>button {
            width: 100%;
            border-radius: 10px;
            background: #00c6ff;
            color: black;
            font-weight: bold;
        }

        /* Radio buttons */
        div[role="radiogroup"] {
            display: flex;
            justify-content: center;
            gap: 2rem;
        }

        /* Hide Streamlit footer */
        footer {
            visibility: hidden;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
