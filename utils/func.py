# -*- coding: utf-8 -*-

import datetime
from dateutil.relativedelta import relativedelta

import os.path
import json

import smtplib
from email.message import EmailMessage
from email.utils import formataddr
from email.header import Header

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
            try:
                creds.refresh(Request())
            except Exception as e:
                print(f"An error occurred: {e}")
                os.remove("token.json")
                return google_sync()
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)

    with open("token.json", "w") as token:
        token.write(creds.to_json())

    print("Sync Google OK")
    return build("calendar", "v3", credentials=creds)


def get_json_key(key):
    with open("config.json", "r") as file:
        config = json.load(file)

    return config.get(key)


def timer_start():
    print("Timer start")
    with open("tmp.txt", "w") as file:
        file.write(str(datetime.datetime.now()))
    return datetime.datetime.now()


def timer_stop(service_google, start_time):
    end_time = datetime.datetime.now()

    event = {
        "summary": "Degecom",
        "start": {"dateTime": start_time.isoformat(), "timeZone": "Europe/Paris"},
        "end": {"dateTime": end_time.isoformat(), "timeZone": "Europe/Paris"},
    }

    try:
        service_google.events().insert(calendarId=get_json_key("calendarId"), body=event).execute()
    except HttpError as e:
        print(f"An error occurred: {e}")
    
    if os.path.exists("tmp.txt"):
        os.remove("tmp.txt")

    print("Event added")


def get_events(service_google):
    now = datetime.datetime.now()
    start = datetime.datetime(now.year, now.month, 1)
    end = start + relativedelta(months=1)

    startIso = start.isoformat() + 'Z'
    endIso = end.isoformat() + 'Z'

    events_result = (service_google.events().list(
        calendarId=get_json_key("calendarId"),
        timeMin=startIso,
        timeMax=endIso,
        orderBy="startTime",
        singleEvents=True,
    ).execute())
    
    return events_result.get("items", [])


def get_hours(service_google) -> str:
    infos = {"start": [], "end": [], "duration": []}
    
    events = get_events(service_google)
    if events:
        for event in events:
            infos["start"] += [event["start"].get("dateTime", event["start"].get("date"))]
            infos["end"] += [event["end"].get("dateTime", event["end"].get("date"))]
            infos["duration"] += [datetime.datetime.fromisoformat(infos["end"][-1]) - datetime.datetime.fromisoformat(infos["start"][-1])]
    
    return infos
    

def generate_report(service_google):
    now = datetime.datetime.now()
    total = datetime.timedelta()

    filename = "hours_report_" + now.strftime("%B") + ".csv"
    with open(filename, "w") as file:
        file.write("N°,Début,Fin,Durée\n")

        infos = get_hours(service_google)
        for nb, (start, end, duration) in enumerate(zip(infos["start"], infos["end"], infos["duration"]), 1):
            file.write(f"{nb},{start},{end},{duration}\n")
            total += duration
 
        file.write(f"Total,,,{total.days * 24 + total.seconds // 3600}:{(total.seconds % 3600) // 60:02}:{total.seconds % 60:02}\n")

    msg = EmailMessage()
    msg["Subject"] = "Rapport mensuel"
    msg["From"] = formataddr((str(Header(get_json_key("name"), "utf-8")), get_json_key("email_user")))
    msg["To"] = get_json_key("email_recipient")
    if get_json_key("email_cc"):
        msg["Cc"] = get_json_key("email_cc")

    msg.add_alternative("<p>Veuillez trouver ci-joint le rapport détaillée de toutes les heures que j'ai effectuée durant ce mois.</p>" + get_json_key("email_signature"), subtype="html")

    with open(filename, "rb") as file:
        msg.add_attachment(file.read(), maintype="text", subtype="csv", filename=filename)

    srv = smtplib.SMTP(get_json_key("email_host"), 587)
    srv.starttls()
    srv.login(get_json_key("email_user"), get_json_key("email_password"))
    srv.send_message(msg)
    srv.quit()

    os.remove(filename)
    
    print("Report sent")


def is_time():
    if os.path.exists("tmp.txt"):
        with open("tmp.txt", "r") as file:
            return datetime.datetime.fromisoformat(file.read())
    return None