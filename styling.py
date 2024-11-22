import streamlit as st

def add_background_style():
    st.markdown(
        """
        <style>
        body {font-size:1.2rem}
        .main { background: linear-gradient(135deg, #cccccc 50%, #2ecc71 50%); color: #333; }
        .css-18e3th9 { padding: 2rem 3rem; max-width: 900px; margin: auto; }
        .css-1d391kg { background-color: #ffffff !important; border-radius: 10px; }
        .stTextInput > div > input { border-radius: 8px; padding: 0.5rem; font-size: 1rem; border: 1px solid #ccc; }
        .stMarkdown { border-radius: 8px; padding: 1rem; margin-bottom: 1rem; }
        </style>
        """,
        unsafe_allow_html=True
    )
