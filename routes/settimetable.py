from flask import Blueprint, request, jsonify
from datetime import timedelta , date
import json
from utils.google_calendar import create_google_calendar_service as google_calendar
from utils.timetable import timetable as timetable

settimetable_bp = Blueprint('settimetable', __name__)

@settimetable_bp.route("/settimetable", methods=["GET" , "POST"])
def set_timetable():
    if request.method == "GET":
        return "Use Post with token"
    elif request.method == "POST":
        data = request.json
        
        task = data.get("task")
        token = data.get("token")

        if not task:
            return jsonify({"error" : "Task is required"}) , 400
        
        tt = timetable(task)
        tt = json.loads(tt)

        response_calendar = google_calendar(token)
        service = response_calendar[0]
        creds = response_calendar[1]

        start_date = date.today()

        if "error" in tt[0]:
            return jsonify({"error" : tt[0]["error"]}) , 500 

        response = ""
        try:
            for item in tt:
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

                created_event = service.events().insert(calendarId='primary', body=event).execute()

                response = response + f"Event created: {created_event['summary']} on {created_event['start']['dateTime']}"+ " <br>"

            return jsonify({"token" : str(creds) , "response" : response})
        except Exception as e:
            print("Error Creating event : " , str(e))
            return jsonify({"error" : str(e)}) , 500 