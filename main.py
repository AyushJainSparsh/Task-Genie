import streamlit as st
from mongodb import signin , signup , task

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "page" not in st.session_state:
    st.session_state.page = "signin"

if st.session_state.page == "signin":
    signin.signin()
elif st.session_state.page == "signup":
    signup.signup()

# If authenticated, display the main app
elif st.session_state.authenticated:
    task.task_manager()





# st.session_state.clear()
# to log out