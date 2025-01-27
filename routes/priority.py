from flask import Blueprint, request, jsonify 
from utils.gemini_client import get_gemini_model # gives a gemini model

priority_bp = Blueprint('priority', __name__)

@priority_bp.route("/recommendpriority", methods=["GET" , "POST"])
def recommendpriority():
    if request.method == "GET":
        return "Use POST with task"
    elif request.method == "POST":
        data = request.json
        task = data.get("task")

        if not task:
            return jsonify({"error" : "Task is required"}) , 400
        
        model = get_gemini_model()

        try:
            chat_session = model.start_chat(
                history = [
                    {
                        "role": "user", 
                        "parts": [
                            {"text": "Just give me the priority of the task I am giving to you in high, medium, or low; otherwise, respond 'not a task' in one word (any other word is restricted)."}
                        ]
                    }
                ]
            )
            response = chat_session.send_message(task)
            return jsonify({"priority" : response.text})
        except Exception as e:
            return jsonify({"error" : str(e)}) , 500