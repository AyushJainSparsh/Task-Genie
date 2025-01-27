from flask import Blueprint, request, jsonify
from utils.gemini_client import get_gemini_model  # Import Gemini model from utils

recommend_bp = Blueprint('recommend', __name__)  # Create a new blueprint for this route

@recommend_bp.route("/recommend", methods=["GET" , "POST"])
def recommend():
    if request.method == "GET":
        return "Use POST with task and query in the body"
    elif request.method == "POST":
        data = request.json
        task = data.get("task")
        query = data.get("query")

        if not task or not query:
            return jsonify({"error": "Task and query are required"}), 400

        model = get_gemini_model()

        try:
            chat_session = model.start_chat(
                history=[
                    {"role": "user",
                    "parts": [
                        {
                            "text": f"Resolve the user query related to this task: {task}"
                            +"(Provide output in simple format like without using bold letters or any such things and give only output and where we have to change line add a HTML line changing tag their only)."
                            }
                        ]
                    }
                ]
            )
            response = chat_session.send_message(query)
            return jsonify({"recommendation": response.text})
        except Exception as e:
            return jsonify({"error": str(e)}), 500