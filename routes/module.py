from flask import Blueprint, request, jsonify
import typing_extensions as typing
import json
from utils.gemini_client import get_gemini_model

module_bp = Blueprint('module', __name__)

class Module(typing.TypedDict):
    header : str
    module_inside_info : str
    module : int

@module_bp.route("/recommendmodule", methods=["GET" , "POST"])
def recommend_module():
    if request.method == "GET" :
        return "Use POST with task"
    elif request.method == "POST":
        data = request.json
        task = data.get("task")

        if not task:
            return jsonify({"error" : "Task is required"}) , 400

        module_config = {
            "temperature": 1,
            "top_p": 0.95,
            "top_k": 40,
            "max_output_tokens": 8192,
            "response_mime_type": "application/json",
            "response_schema" : list[Module]
        }

        # Get the Gemini model with the module configuration
        model = get_gemini_model(module_config)

        try :
            chat_session = model.start_chat(
                history = [{
                    "role" : "user" ,
                    "parts" : [{
                        "text" : '''Divide my task into modules from a very basic level to advance in such a way that user have no idea about it 
                        so provide a detail regards every module also and make it easier for user .

                        In json format you have to arrange things as like,

                        header : the header which consists of the above part of starting a module.
                        module : contains the module number.
                        module_inside_info : contains everything inside a single module in detail as user have null knowledge regards the task.
                        '''
                    }]
                }]
            )
            response = chat_session.send_message(task)

            json_output = json.loads(response.text)
            response = json_output
            
            res = ""
            for o in response:
                res = res + f'{o["header"]}' + ' <br> ' + f'Module : {o["module"]}' + ' <br> ' + o["module_inside_info"] + '<br> <br> '


            return jsonify({"module" : res})
        except Exception as e:
            return jsonify({"error" : str(e)}) , 500
