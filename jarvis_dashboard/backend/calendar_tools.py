# calendar_tools.py
import datetime
import os
import pickle
from zoneinfo import ZoneInfo  # Python 3.9+; if using an older version, use pytz
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from zoneinfo import ZoneInfo
from dotenv import load_dotenv
load_dotenv()

# If modifying these scopes, delete your token file.
SCOPES = ['https://www.googleapis.com/auth/calendar']

class GoogleCalendarManager:
    def __init__(self, credentials_path='credentials.json', token_path='token.pickle', tz='America/Chicago'):
        self.credentials_path = credentials_path
        self.token_path = token_path
        self.tz = tz  # local time zone string; change to your local zone if needed.
        self.creds = None
        self.service = self.authenticate()

    def authenticate(self):
        if os.path.exists(self.token_path):
            with open(self.token_path, 'rb') as token:
                self.creds = pickle.load(token)
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(self.credentials_path, SCOPES)
                self.creds = flow.run_local_server(port=0)
            with open(self.token_path, 'wb') as token:
                pickle.dump(self.creds, token)
        return build('calendar', 'v3', credentials=self.creds)

    def add_event(self, summary, start_time, end_time, description=""):
        event = {
            'summary': summary,
            'description': description,
            'start': {
                'dateTime': start_time,  # ISO format string in local time
                'timeZone': 'America/Chicago'
            },
            'end': {
                'dateTime': end_time,
                'timeZone': 'America/Chicago'
            }
        }
        event = self.service.events().insert(calendarId='primary', body=event).execute()
        return event

    def get_events_for_day(self, day_str="today"):
        if day_str.lower() == "today":
            target_date = datetime.datetime.now(ZoneInfo(self.tz)).date()
        else:
            try:
                target_date = datetime.datetime.strptime(day_str, "%Y-%m-%d").date()
            except Exception as e:
                return f"Error parsing date: {e}"
        start_of_day = datetime.datetime.combine(target_date, datetime.time.min, tzinfo=ZoneInfo(self.tz))
        end_of_day = datetime.datetime.combine(target_date, datetime.time.max, tzinfo=ZoneInfo(self.tz))
        start_iso = start_of_day.isoformat()
        end_iso = end_of_day.isoformat()
        events_result = self.service.events().list(
            calendarId='primary', timeMin=start_iso, timeMax=end_iso,
            singleEvents=True, orderBy='startTime').execute()
        events = events_result.get('items', [])
        return events

    def get_events_for_date_range(self, start_date_str, end_date_str):
        try:
            start_date = datetime.datetime.strptime(start_date_str, "%Y-%m-%d").date()
            end_date = datetime.datetime.strptime(end_date_str, "%Y-%m-%d").date()
        except Exception as e:
            return f"Error parsing dates: {e}"
        start_dt = datetime.datetime.combine(start_date, datetime.time.min, tzinfo=ZoneInfo(self.tz))
        end_dt = datetime.datetime.combine(end_date, datetime.time.max, tzinfo=ZoneInfo(self.tz))
        start_iso = start_dt.isoformat()
        end_iso = end_dt.isoformat()
        events_result = self.service.events().list(
            calendarId='primary', timeMin=start_iso, timeMax=end_iso,
            singleEvents=True, orderBy='startTime').execute()
        events = events_result.get('items', [])
        return events

# Instantiate the calendar manager globally.
calendar_manager = GoogleCalendarManager()

def format_events(events, period_description=""):
    if isinstance(events, str):
        return events
    if not events:
        return f"You have no events scheduled for {period_description}."
    response = f"Events for {period_description}:\n"
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        response += f"- {event.get('summary', 'No Title')} at {start}\n"
    return response

def get_calendar_events(day="today"):
    events = calendar_manager.get_events_for_day(day)
    return format_events(events, day)

def get_calendar_events_range(start_date, end_date):
    events = calendar_manager.get_events_for_date_range(start_date, end_date)
    return format_events(events, f"{start_date} to {end_date}")

def get_calendar_events_for_week(reference_date="today"):
    if reference_date.lower() == "today":
        ref = datetime.datetime.now(ZoneInfo(calendar_manager.tz)).date()
    else:
        try:
            ref = datetime.datetime.strptime(reference_date, "%Y-%m-%d").date()
        except Exception as e:
            return f"Error parsing reference date: {e}"
    monday = ref - datetime.timedelta(days=ref.weekday())
    sunday = monday + datetime.timedelta(days=6)
    return get_calendar_events_range(monday.isoformat(), sunday.isoformat())

def add_calendar_event(summary, start_time, end_time, description=""):
    try:
        event = calendar_manager.add_event(summary, start_time, end_time, description)
        return f"Event '{event.get('summary', 'No Title')}' added on {event['start'].get('dateTime', 'unknown time')}."
    except Exception as e:
        return f"Error adding event: {e}"

def delete_calendar_event(summary, day="today"):
    events = calendar_manager.get_events_for_day(day)
    if isinstance(events, str):
        return events
    if not events:
        return f"No events scheduled for {day}."
    for event in events:
        if summary.lower() in event.get('summary', '').lower():
            event_id = event['id']
            try:
                calendar_manager.service.events().delete(calendarId='primary', eventId=event_id).execute()
                return f"Event '{event.get('summary')}' has been deleted."
            except Exception as e:
                return f"Error deleting event: {e}"
    return f"No event with summary '{summary}' found on {day}."

def update_calendar_event(old_summary, new_summary, new_start_time, new_end_time, description=""):
    """
    Update an event by deleting the old one (matching old_summary) and adding a new event with the updated details.
    Assumes the event to update is on the day derived from new_start_time.
    """
    # Determine the day from the new_start_time (assuming ISO format, e.g., "2025-02-05T10:00:00")
    try:
        new_start_dt = datetime.datetime.fromisoformat(new_start_time)
        day_str = new_start_dt.date().isoformat()
    except Exception as e:
        return f"Error parsing new start time: {e}"
    
    # First, delete the old event (you might want to refine matching criteria)
    deletion_result = delete_calendar_event(old_summary, day=day_str)
    
    # Check if deletion was successful (you might check for the word "deleted")
    if "deleted" not in deletion_result.lower():
        return f"Failed to update event: {deletion_result}"
    
    # Now, add the new event with the updated details
    addition_result = add_calendar_event(new_summary, new_start_time, new_end_time, description)
    return f"Updated event: {addition_result}"
