from pymongo import MongoClient
import streamlit as st
import os
import gemini.analyze as anal
from dotenv import load_dotenv
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request # to send request to refresh token
import os
from datetime import datetime , timedelta , date
import json

load_dotenv()

# MongoDB Connection
#mongo_uri = os.getenv("MONGO_URI")
#client = MongoClient(mongo_uri)
client = MongoClient(st.secrets["MONGO_URI"] , tls=True, tlsAllowInvalidCertificates=False,)
db = client["todopro"]
users_collection = db["users"]
tasks_collection = db["tasks"]

def task_manager():
    if "user" not in st.session_state:
        st.warning("Please sign in to manage your tasks.")
        st.session_state.authenticated = False
        st.session_state.page = "signin"
        return

    st.title("Task Manager")
    user = st.session_state["user"]
    user_id = user["_id"]

    # Add Task
    
    task = st.text_input("Enter a task")
    if st.button("Add Task"):
        prior = anal.recommend_priority(task)
        roadmap = anal.recommend_roadmap(task)
        module = anal.recommend_module(task)
        tasks_collection.insert_one({"user_id": user_id, "task": task, "status": "pending" , "priority" : prior ,
                                     "roadmap" : roadmap , "module" : module})
        st.success("Task added!")
    st.write("--------------------------------------------------------------------------------------------------------------------------")
    
    
    # Display Tasks

    
    pending_tasks = list(tasks_collection.find({"user_id": user_id, "status": "pending"}))
    if pending_tasks is not None:
        st.subheader("Your Tasks")
        
        for t in pending_tasks:
            st.write(f"- {t['task']} (Priority: {t['priority']}) (Status: {t['status']})")
    st.write("--------------------------------------------------------------------------------------------------------------------------")

    # add calender 

    task_table = st.selectbox("Select Task" , [task["task"] for task in pending_tasks])

    if st.button("Add TimeTable"):

        client_json = st.secrets["CLIENT_SECRET"]

        with open('client_secret.json' , 'w') as file:
            json.dump(json.loads(client_json) , file)

        creds = None
        SCOPES = ['https://www.googleapis.com/auth/calendar']

        user = users_collection.find_one({"_id": user_id})

        token = user.get("email_token_json")

        if user and user.get("email_token_json"):
            with open('token.json' , 'w') as file:
                json.dump(json.loads(token) , file)

            # Check if the token.json file exists to get stored credentials
            if token != "none" and os.path.exists('token.json'):
                creds = Credentials.from_authorized_user_file('token.json', SCOPES)

        # If there are no (valid) credentials, prompt the user to log in
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                # Refresh the token if expired
                creds.refresh(Request())
            else:
                # Run the OAuth flow to get new credentials
                flow = InstalledAppFlow.from_client_secrets_file(
                    #'mongodb/client_secret.json',
                    "client_secret.json" ,
                     SCOPES)
                creds = flow.run_local_server(port=8080)

            # Save the credentials to token.json for future use
            users_collection.update_one({"_id" : user_id} , {"$set" : {"email_token_json" : creds.to_json()}})

        # Create the Google Calendar service
        service = build('calendar', 'v3', credentials=creds)

        timetable = anal.timetable(task_table)

        start_date = date.today()

        for item in timetable:
            # Calculate the event date
            event_date = start_date + timedelta(days=item['day'] - 1)  # Day 1 is the starting date
            
            # Create the event
            event = {
                'summary': item['task'],
                'start': {
                    'dateTime': event_date.isoformat() + 'T17:00:00',  # Starting at 9 AM (you can change the time)
                    'timeZone': 'Asia/Kolkata',  # Set time zone for India
                },
                'end': {
                    'dateTime': event_date.isoformat() + 'T18:00:00',  # Ending at 10 AM (you can adjust the duration)
                    'timeZone': 'Asia/Kolkata',
                },
            }

            # Insert the event into the calendar
            created_event = service.events().insert(calendarId='primary', body=event).execute()
            st.write(f"Event created: {created_event['summary']} on {created_event['start']['dateTime']}")

    st.write("----------------------------------------------------------------------------------------------------------------------")


    # Mark Task as Done
    
    
    done_task = st.selectbox("Mark task as done" , [task["task"] for task in pending_tasks])
    if st.button("Complete Task"):
        result = tasks_collection.update_one({"user_id": user_id, "task": done_task}, {"$set": {"status": "completed"}})
        if result.modified_count:
            st.success("Task marked as completed!")
    st.write("--------------------------------------------------------------------------------------------------------------------------")
    
    
    # Display completed tasks in a dropdown
    completed_tasks = list(tasks_collection.find({"user_id": user_id, "status": "completed"}))
    if not completed_tasks:
        st.info("You have no completed tasks to delete.")

    task_to_delete = st.selectbox(
        "Select a task to delete", [task["task"] for task in completed_tasks]
    )
    # Delete the selected task when button is clicked
    if st.button("Delete Task"):
        tasks_collection.delete_one({"user_id": user_id, "task": task_to_delete, "status": "completed"})
        st.success(f"Task '{task_to_delete}' has been deleted.")
    st.write("--------------------------------------------------------------------------------------------------------------------------")


    # Detailed Roadmap

    pending_tasks = list(tasks_collection.find({"user_id": user_id, "status": "pending"}))
    st.subheader("Detailed Roadmap")
    task_list = [task["task"] for task in pending_tasks]
    task = st.selectbox("Select your task" , task_list)
    if st.button("Roadmap"): 
        for i in range(len(pending_tasks)):
            if(task == pending_tasks[i]["task"]):
                st.write(pending_tasks[i]["roadmap"])
                st.write(pending_tasks[i]["module"])
    st.write("--------------------------------------------------------------------------------------------------------------------------")


    # Query


    st.subheader("Query about Roadmap or Task")
    t = st.selectbox("Select your task" , [task["task"] for task in pending_tasks] , key="Query")
    query = st.text_input("Write your Query : ")
    if st.button("Recommend"):
        if query == "":
            st.error("enter query first")
        else:
            st.write(anal.recommend(t , query))


    st.write("--------------------------------------------------------------------------------------------------------------------------")

    #SignOut
    if st.button("Sign Out"):
        st.session_state.clear()

