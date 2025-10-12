
import streamlit as st
import pandas as pd
import os

# Passwords (demo only - replace with env vars or hashed auth in production)
STAFF_PASSWORD = "staff123"
LEARNER_PASSWORD = "learner123"

def staff_login():
    st.subheader("🔐 Staff Login")
    password = st.text_input("Enter staff password:", type="password")
    if password == STAFF_PASSWORD:
        return True
    elif password:
        st.error("❌ Incorrect password")
    return False

def learner_login():
    st.subheader("🎓 Learner Login")
    password = st.text_input("Enter learner password:", type="password")
    if password == LEARNER_PASSWORD:
        return True
    elif password:
        st.error("❌ Incorrect password")
    return False

def read_leads(file_path):
    if os.path.exists(file_path):
        return pd.read_csv(file_path, header=None, names=["Name", "Email", "Level", "Schedule/Message"])
    return pd.DataFrame(columns=["Name", "Email", "Level", "Schedule/Message"])
