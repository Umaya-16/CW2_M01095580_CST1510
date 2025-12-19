import streamlit as st
from app.log_hash import hash_password, valid_hash, validate_username, validate_password
from app.users import add_user, get_user
from app.db import get_db_connection

# connect to the database
conn = get_db_connection()

# page setup
st.set_page_config(page_title="Home Page", page_icon="🏡", layout="wide")

# check login state
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

st.header("Home Page")
st.write("Welcome to the home page of the application")

# tabs for login and register
tab_login, tab_register = st.tabs(["Login", "Register"])

# LOGIN TAB
with tab_login:
    login_name = st.text_input("Username: ", key="login_username")
    login_password = st.text_input("Password", type="password", key="login_password")

    if st.button("Log In", key="login_button"):
        if not login_name.strip() or not login_password.strip():
            st.error("Please enter both username and password.")
        else:
            user = get_user(conn, login_name)
            if user:
                id, name, hash = user
                if name == login_name and valid_hash(login_password, hash):
                    st.session_state["logged_in"] = True
                    st.session_state["username"] = login_name  # save username for dashboard
                    st.success("You are now logged in.")
                    st.switch_page("pages/dashboard.py")  # redirect to dashboard
                else:
                    st.error("Invalid username or password.")
            else:
                st.error("User not found.")

# REGISTER TAB
with tab_register:
    st.info("Registration: ")
    reg_name = st.text_input("Username: ", key="register_username")
    reg_password = st.text_input("Password", type="password", key="register_password")
    reg_password_confirm = st.text_input("Confirm Password", type="password", key="register_password_confirm")

    if st.button("Register", key="register_button"):
        if not reg_name.strip() or not reg_password.strip() or not reg_password_confirm.strip():
            st.error("Please fill in all fields before registering.")
        elif not validate_username(reg_name):
            st.error("Invalid username. Must be at least 3 characters and alphanumeric.")
        elif not validate_password(reg_password):
            st.error("Weak password. Must be at least 8 characters, include uppercase, lowercase, number, and symbol.")
        elif reg_password != reg_password_confirm:
            st.error("Passwords do not match.")
        else:
            hashed_psw = hash_password(reg_password)
            add_user(conn, reg_name, hashed_psw)
            st.success("Registration successful!")