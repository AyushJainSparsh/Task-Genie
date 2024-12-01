from pymongo import MongoClient
import streamlit as st
import os
import gemini.analyze as anal

# MongoDB Connection
#mongo_uri = os.getenv("MONGO_URI")
#client = MongoClient(mongo_uri)
client = MongoClient(st.secrets["MONGO_URI"] , tls=True,
        tlsAllowInvalidCertificates=False,)
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

