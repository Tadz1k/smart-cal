# -*- coding: utf-8 -*-

import datetime
import os.path
from Models.Event import Event

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

class Google_Integration:
    
  def __init__(self):
    # If modifying these scopes, delete the file token.json.
    self.SCOPES = ["https://www.googleapis.com/auth/calendar"]
    self.creds = self.authorize()
    self.service = build("calendar", "v3", credentials=self.creds)

  def authorize(self):
    creds = None
    if os.path.exists("token.json"):
      creds = Credentials.from_authorized_user_file("token.json", self.SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
      if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
      else:
        flow = InstalledAppFlow.from_client_secrets_file(
            "conf.json", self.SCOPES
        )
        creds = flow.run_local_server(port=0)
      # Save the credentials for the next run
      with open("token.json", "w") as token:
        token.write(creds.to_json())
    return creds
  
  
  def add_event(self, event):
    event = {
      "summary": event.name,
      "location": event.location,
      "start": {
        "dateTime": event.start_time.isoformat(),
        "timeZone": "Europe/Warsaw",
      },
      "end": {
        "dateTime": event.end_time.isoformat(),
        "timeZone": "Europe/Warsaw",
      },
    }
    events_result = self.service.events().insert(calendarId="primary", body=event).execute()
    
    
  
  
  def get_events(self):
    try:

      # Call the Calendar API
      now = datetime.datetime.utcnow()

      start_of_month = datetime.datetime(now.year, now.month, 1)
      if now.month == 12:  # If current month is december
          end_of_month = datetime.datetime(now.year + 1, 1, 1, 0, 0, 0) - datetime.timedelta(days=1)
      else:
          end_of_month = datetime.datetime(now.year, now.month + 1, 1, 0, 0, 0) - datetime.timedelta(days=1)


      # Formatowanie daty do formatu zgodnego z API
      time_min = start_of_month.isoformat() + "Z"
      time_max = end_of_month.isoformat() + "Z"
      events_result = (
          self.service.events()
          .list(
              calendarId="primary",
              timeMin=time_min,
              timeMax=time_max,
              singleEvents=True,
              orderBy="startTime",
          )
          .execute()
      )
      events = events_result.get("items", [])

      if not events:
        print("No upcoming events found.")
        return

      # Prints the start and name of the next 10 events
      return events

    except HttpError as error:
      print(f"An error occurred: {error}")
