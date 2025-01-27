from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google.auth.transport.requests import Request # to send request to refresh token
from google_auth_oauthlib.flow import InstalledAppFlow
import json
import os

def create_google_calendar_service(token):
    """Creates and returns a Google Calendar service."""
    
    creds = None
    SCOPES = ['https://www.googleapis.com/auth/calendar']


    with open('token.json' , 'w') as file:
        json.dump(token , file)

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
                "client_secret.json" ,
                SCOPES)
            creds = flow.run_local_server(port=8080)

    # Create the Google Calendar service
    return [build('calendar', 'v3', credentials=creds),creds]
