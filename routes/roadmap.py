from flask import Blueprint, request, jsonify 
import typing_extensions as typing
import json
from utils.gemini_client import get_gemini_model # gives a gemini model

roadmap_bp = Blueprint('roadmap', __name__)

class Roadmap(typing.TypedDict):
    format : str
    task : str
    phase : int

@roadmap_bp.route("/recommendroadmap", methods=["GET" , "POST"])
def recommend_roadmap():
    if request.method == "GET":
        return "Use POST with task"
    elif request.method == "POST":
        data = request.json
        task = data.get("task")

        if not task:
            return jsonify({"error" : "Task is required"}) , 400

        # Define a custom configuration for the roadmap route
        roadmap_config = {
            "temperature": 1,
            "top_p": 0.95,
            "top_k": 40,
            "max_output_tokens": 8192,
            "response_mime_type": "application/json",
            "response_schema" : list[Roadmap]
            }

        # Get the Gemini model with the roadmap configuration
        model = get_gemini_model(roadmap_config)

        try:
            chat_session = model.start_chat(
            history=[
                {
                    "role": "user",  # Adjust to "system" or "user" based on your need
                    "parts": [
                        {"text": '''Prepare a roadmap for the provided task on the daily, hourly, weekly or , monthly basis as per need by a task to complete it for basics to deep. 
                        its a strict order that roadmap is only in hourly, daily, weekly or monthly format as per needed by task and the task we have to accomplish in it.
                        
                        in json format you have to arrange things as per given:

                        format : in which basis you set the timetable like weekly , hourly , daily or monthly basis.
                        phase : day , week , hour or month number.
                        task : the task you have to fulfill.

                        Note : Provide output in only one format i.e. if output is in daily format it only be in daily format.
                        '''
                            }
                        ]
                    }
                ]
            )
            response = chat_session.send_message(task)
            response = json.loads(response.text)
            res = ""
            for o in response:
                res = res + f'{o["format"]} : {o["phase"]}' + ' <br> ' + o["task"] + ' <br> <br> '


            return jsonify({"format" : response[0]["format"] , 
                "roadmap" : res})
        except Exception as e:
            return jsonify({"error" : str(e)}) , 500
