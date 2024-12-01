import hashlib
from pymongo import MongoClient
import streamlit as st
import os

# MongoDB Connection
#mongo_uri = os.getenv("MONGO_URI")
#client = MongoClient(mongo_uri)
client = MongoClient(st.secrets["MONGO_URI"] , tls=True,
        tlsAllowInvalidCertificates=False,)
db = client["todopro"]
users_collection = db["users"]

# Hash function for passwords
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Signup Page
def signup():
    st.title("Signup")
    username = st.text_input("Enter a username")
    password = st.text_input("Enter a password", type="password")
    if st.button("Signup"):
        if users_collection.find_one({"username": username}):
            st.warning("Username already exists. Please choose a different username.")
        else:
            hashed_password = hash_password(password)
            users_collection.insert_one({"username": username, "password": hashed_password})
            st.success("Signup successful! You can now sign in.")
            st.session_state.page = "signin"

# Call signup function if needed

