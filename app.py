import os
import streamlit as st
from auth import login_signup_page
from chat import chat_interface
from summarize import summarize_module
from styling import add_background_style
from pdf_processing import upload_pdf_and_process

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

# Configuring the Streamlit page
st.set_page_config("Chat PDF", layout="wide")

def navbar():
    st.sidebar.title("Navigation")
    return st.sidebar.radio("Go to", ["Chat Interface", "Summarize"])

def main():
    add_background_style()
    if 'logged_in' not in st.session_state or not st.session_state['logged_in']:
        login_signup_page()
    else:
        # Sidebar upload and shared PDF processing
        upload_pdf_and_process()
        
        # Navigation choice
        choice = navbar()
        
        st.markdown("<h1 style='font-size:36px; text-align:center'>BriefMe - Ask, Summarize, Explore</h1>", unsafe_allow_html=True)
        if 'pdf_processed' in st.session_state and st.session_state['pdf_processed']:
            if choice == "Chat Interface":
                chat_interface()
            elif choice == "Summarize":
                summarize_module()
        else:
            st.write("Please upload a PDF to use the Chat or Summarize features.")

if __name__ == "__main__":
    main()
