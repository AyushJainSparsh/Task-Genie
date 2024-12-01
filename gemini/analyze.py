import os
import google.generativeai as genai
from dotenv import load_dotenv
import streamlit as st

def configure():
    load_dotenv()
#os.environ["GEMINI_API_KEY"] = "API_KEY"

genai.configure(api_key=st.secrets["GEMINI_API_KEY"]) # also use os.getenv("GEMINI_API_KEY")

# Create the model
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 40,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
  model_name="gemini-1.5-pro",
  generation_config=generation_config,
)

def recommend(task , query):

    # Start a chat session with role-specified history
    chat_session = model.start_chat(
        history=[
            {
                "role": "user",  # Adjust to "system" or "user" based on your need
                "parts": [
                    {"text": "Resolve the user query related to this task : "+task }
                ]
            }
        ]
    )
    try:
        response = chat_session.send_message(query)
        return response.text
    except Exception as e:
        print(f"Error: {e}")
        return "Error: Unable to generate recommendation."

def recommend_priority(task):

    # Start a chat session with role-specified history
    chat_session = model.start_chat(
        history=[
            {
                "role": "user",  # Adjust to "system" or "user" based on your need
                "parts": [
                    {"text": "Just give me the priority of the task I am giving to you in high, medium, or low; otherwise, respond 'not a task' in one word (any other word is restricted)."}
                ]
            }
        ]
    )
    try:
        response = chat_session.send_message(task)
        priority = response.text.strip().lower()  # Normalize the response to lowercase
        if priority in ["high", "medium", "low"]:
            return priority
        else:
            print("Invalid response, defaulting to 'medium'.")
            return "medium"  # Default if the model response doesn't match expected output
    except Exception as e:
        print(f"Error: {e}")
        return "Error: Unable to generate recommendation."
    
def recommend_roadmap(task):

    # Start a chat session with role-specified history
    chat_session = model.start_chat(
        history=[
            {
                "role": "user",  # Adjust to "system" or "user" based on your need
                "parts": [
                    {"text": "Prepare a roadmap for the provided task on the daily basis and hourly to achieve as must fast as a human can."}
                ]
            }
        ]
    )
    try:
        response = chat_session.send_message(task)
        return response.text
    except Exception as e:
        print(f"Error: {e}")
        return "Error: Unable to generate recommendation."
    
def recommend_module(task):

    # Start a chat session with role-specified history
    chat_session = model.start_chat(
        history=[
            {
                "role": "user",  # Adjust to "system" or "user" based on your need
                "parts": [
                    {"text": "Divide my task into modules in a very basic level in such a way that user have no idea about it so provide a detail regards every module also."}
                ]
            }
        ]
    )
    try:
        response = chat_session.send_message(task)
        return response.text
    except Exception as e:
        print(f"Error: {e}")
        return "Error: Unable to generate recommendation."


configure()
'''
task1 = "i want to create a platform where anyone with mere idea and may or may have not have any  technical knowledge can hire a mentor(if they require) who would guide them about how this idea could be made reality.If the user wants to create a team of like minded peeps who have required technical knowledge to make this idea a real working project. After creation of the fully functional prototype the team may post the description of  idea, prototype its all use case and its importance, the field where it may be useful its version control repository(soo that if anyone of the peer user of the platform may find any bugs or have any betterment in there mind could easily clone the repo and do the required changes and could contribute for bounties).Once the overall description with the video, images, other use cases are posted on the platform all other users can upvote the post if they find the prototype and idea useful.The post with major upvotes will be highlighted and grab the attention of investors and fund providers.The  investors may message them personally, they could arrange an online meeting on the platform for further discussions and if everything goes right the developer of the platform could get funding. And hence the platform could be used as a game changer in startup india. The user may also be able to find the collaborative working space near them (if they require) such as incubation centers etc. the user could also get a all the professionals and government agents for  statups registration,idea patent, copy right documentation creation.the plstform would also incliude a workspace where anyone who wants can publish there dataset on the space soo that anyone else who require a same dataset could easily get it"
task2 ="make it concise and in well structured points soo that i could mention it in my project ppt and make sure it describes the project completely"
print(recommend_priority(task1+task2))
print(recommend_roadmap(task1+task2))
print(recommend_module(task1+task2))'''
