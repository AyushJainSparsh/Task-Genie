import hashlib
from pymongo import MongoClient
import streamlit as st
import os

# MongoDB Connection
#mongo_uri = os.getenv("MONGO_URI")
#client = MongoClient(mongo_uri)
client = MongoClient(st.secrets["MONGO_URI"], tls=True,
        tlsAllowInvalidCertificates=False,)
db = client["todopro"]
users_collection = db["users"]


# Hash function for passwords
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Signin Page
def signin():
    st.title("Sign In")
    username = st.text_input("Enter your username")
    password = st.text_input("Enter your password", type="password")
    if st.button("Signin"):
        user = users_collection.find_one({"username": username})
        if user and user["password"] == hash_password(password):
            st.success(f"Welcome, {username}!")
            st.session_state["user"] = user  # Store user details in session
            st.session_state.authenticated = True
            st.session_state.page = "task_manager"
        else:
            st.error("Invalid username or password.")        
    if st.button("Sign Up"):
        st.session_state.page = "signup"
