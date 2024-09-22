# -*- coding: utf-8 -*-

import datetime
from dateutil.relativedelta import relativedelta
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


def generate_report(service_google):
    now = datetime.datetime.now()
    start = datetime.datetime(now.year, now.month, 1)
    end = start + relativedelta(months=1) - relativedelta(days=2)

    startIso = start.isoformat() + 'Z'
    endIso = end.isoformat() + 'Z'

    events_result = (service_google.events().list(
        calendarId=get_calendar_id(),
        timeMin=startIso,
        timeMax=endIso,
        orderBy="startTime",
        singleEvents=True,
    ).execute())
    events = events_result.get("items", [])

    if not events: return

    total = datetime.timedelta()
    with open("hours_report_" + now.strftime("%B") + ".csv", "w") as file:
        file.write("N°,Début,Fin,Durée\n")
        for nb, event in enumerate(events, 1):
            start = event["start"].get("dateTime", event["start"].get("date"))
            end = event["end"].get("dateTime", event["end"].get("date"))
            duration = datetime.datetime.fromisoformat(end) - datetime.datetime.fromisoformat(start)
            total += duration
            
            file.write(f"{nb},{start},{end},{duration}\n")

        file.write(f"Total,,,{total}\n")