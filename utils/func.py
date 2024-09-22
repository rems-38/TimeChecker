# -*- coding: utf-8 -*-

import datetime
import os.path
import json

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ["https://www.googleapis.com/auth/calendar.events"]


def google_sync():
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)

        with open("token.json", "w") as token:
            token.write(creds.to_json())

    print("Sync Google OK")
    return build("calendar", "v3", credentials=creds)


def get_calendar_id():
    with open("config.json", "r") as file:
        config = json.load(file)

    return config.get("calendarId", "primary")


def timer_start():
    print("Timer start")
    return datetime.datetime.now()


def timer_stop(service_google, start_time):
    end_time = datetime.datetime.now()

    event = {
        "summary": "Degecom",
        "start": {"dateTime": start_time.isoformat(), "timeZone": "Europe/Paris"},
        "end": {"dateTime": end_time.isoformat(), "timeZone": "Europe/Paris"},
    }

    try:
        service_google.events().insert(calendarId=get_calendar_id(), body=event).execute()
    except HttpError as e:
        print(f"An error occurred: {e}")
    
    print("Event added")


def generate_report():
    print("Génération du rapport mensuel...")


