import typing_extensions as typing
import json
from utils.gemini_client import get_gemini_model

class Timetable(typing.TypedDict):
    day : int
    task : str

def timetable(task):
    # Create the model
    timetable_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "application/json",
    "response_schema" : list[Timetable]
    }

    model = get_gemini_model(timetable_config)

    chat_session = model.start_chat(
        history = [
            {
                'role' : 'user',
                'parts' : [
                    {
                        'text' :"""
                            Prepare a timetable for the task provided to complete it in the days required to complete it fully from basics 
                            to depth.

                            the output should be in the the given format:
                            day : day number , e.g. , day = 1 or day = 2
                            task : the task to be accompilshed in that day respectively.

                            there is no boundation of time to complete the task. the main goal is to complete task in a very effective way.
                        """
                    }
                ]
            }
        ]
    )

    try : 
        response = chat_session.send_message(task)
        return response.text
    except Exception as e : 
        print(str(e))
        return {"error " : e}
