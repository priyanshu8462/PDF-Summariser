import streamlit as st

# Placeholder user database
users_db = {
    "test@example.com": {"name": "Test User", "password": "password123"},
    "priyanshu20202@gmail.com": {"name": "Priyanshu", "password": "password123"},
    "test@gmail.com": {"name": "Mohit", "password": "test123"}
}

def login_signup_page():
    st.title("Login / Signup")
    choice = st.selectbox("Choose Action", ["Login", "Signup"])
    
    if choice == "Signup":
        st.subheader("Create a New Account")
        email = st.text_input("Email")
        name = st.text_input("Name")
        password = st.text_input("Password", type="password")
        if st.button("Signup"):
            if email in users_db:
                st.success("Signup successful! Please log in.")
            else:
                users_db[email] = {"name": name, "password": password}
                st.success("Signup successful! Please log in.")
    
    if choice == "Login":
        st.subheader("Login to Your Account")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            user = users_db.get(email)
            if user and user["password"] == password:
                st.session_state['logged_in'] = True
                st.session_state['user'] = user
                st.success(f"Welcome {user['name']}!")
                st.experimental_rerun()
            else:
                st.error("Invalid email or password.")
