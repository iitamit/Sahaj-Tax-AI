# auth.py - Handles Login & Registration
import streamlit as st
import json
import os

DB_FILE = "users_db.json"

def load_users():
    """Loads users from a local JSON file (Persistent Storage)"""
    if not os.path.exists(DB_FILE):
        # Default fallback if file doesn't exist
        return {"admin": "admin123", "user": "user123"}
    try:
        with open(DB_FILE, "r") as f:
            return json.load(f)
    except:
        return {"admin": "admin123", "user": "user123"}

def save_new_user(username, password):
    """Registers a new user"""
    users = load_users()
    if username in users:
        return False # User already exists
    
    users[username] = password
    with open(DB_FILE, "w") as f:
        json.dump(users, f)
    return True

def check_login(username, password):
    """Verifies credentials"""
    users = load_users()
    if username in users and users[username] == password:
        return "admin" if username == "admin" else "user"
    return None

def login_screen():
    """New Tabbed Interface for Login / Sign Up"""
    
    # Create Tabs
    tab_login, tab_signup = st.tabs(["🔑 Sign In", "📝 Sign Up"])

    # --- TAB 1: LOGIN ---
    with tab_login:
        st.markdown("#### Welcome Back")
        l_user = st.text_input("Username", key="login_user")
        l_pass = st.text_input("Password", type="password", key="login_pass")
        
        if st.button("Login Securely", type="primary"):
            role = check_login(l_user, l_pass)
            if role:
                st.session_state["logged_in"] = True
                st.session_state["role"] = role
                st.session_state["username"] = l_user
                st.rerun()
            else:
                st.error("❌ Incorrect Username or Password")

    # --- TAB 2: SIGN UP ---
    with tab_signup:
        st.markdown("#### New Registration")
        r_user = st.text_input("Choose Username", key="reg_user")
        r_pass = st.text_input("Choose Password", type="password", key="reg_pass")
        
        if st.button("Create Account"):
            if r_user and r_pass:
                if save_new_user(r_user, r_pass):
                    st.success("✅ Account Created! Please switch to 'Sign In' tab.")
                else:
                    st.error("⚠️ Username already taken.")
            else:
                st.warning("⚠️ Please fill all fields.")

def logout_button():
    if st.sidebar.button("🚪 Logout"):
        st.session_state["logged_in"] = False
        st.session_state["role"] = None
        st.rerun()