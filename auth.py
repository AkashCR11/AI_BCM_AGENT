import streamlit as st

# ✅ Dummy users (you can replace with DB later)
USERS = {
    "admin": "admin123",
    "user": "user123"
}


def login():
    st.title("🔐 Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username in USERS and USERS[username] == password:
            st.session_state.logged_in = True
            st.session_state.user = username
            st.success("✅ Login successful")
            st.rerun()
        else:
            st.error("❌ Invalid credentials")


def logout():
    if st.sidebar.button("🚪 Logout"):
        st.session_state.logged_in = False
        st.session_state.user = None
        st.rerun()
