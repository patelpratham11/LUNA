from __future__ import print_function
import os
import datetime
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from dateparser.search import search_dates
from datetime import datetime, timedelta
from datetime import datetime
from dateparser.search import search_dates
from datetime import datetime, timedelta
from dateparser.search import search_dates

def get_days_range_from_query(query: str, default_days: int = 7):
    query_lower = query.lower()
    now = datetime.now()

    # These mean the user wants a duration of time
    if "today" in query_lower:
        return 1
    if "tomorrow" in query_lower:
        return 1
    if "next week" in query_lower:
        return 7
    if "this weekend" in query_lower or "the weekend" in query_lower or "weekend" in query_lower:
        return 3
    if "few days" in query_lower or "couple days" in query_lower:
        return 3
    if "this month" in query_lower:
        end_of_month = now.replace(day=28) + timedelta(days=4)
        end_of_month = end_of_month.replace(day=1) - timedelta(days=1)
        return (end_of_month - now).days
    if "next month" in query_lower:
        next_month = now.replace(day=28) + timedelta(days=4)
        first_day_next_month = next_month.replace(day=1)
        end_of_next_month = (first_day_next_month.replace(day=28) + timedelta(days=4)).replace(day=1) - timedelta(days=1)
        return (end_of_next_month - first_day_next_month).days

    # Skip if the user is asking "when is X" — that’s a lookup, not a range
    if "when is" in query_lower or "what day is" in query_lower:
        return 0

    # Only use dateparser if it's likely a date range is being referenced
    parsed = search_dates(query, settings={'PREFER_DATES_FROM': 'future'})
    print(parsed)
    if parsed:
        future_dates = [dt for _, dt in parsed if dt > now]
        if future_dates:
            delta_days = (max(future_dates) - now).days
            print(max(1, delta_days))
            return max(1, delta_days)

    # Still fallback
    return 0


# The scopes required for the Calendar API.
SCOPES = ['https://www.googleapis.com/auth/calendar']

def get_calendar_service():
    """Authenticate and return a Google Calendar service instance."""
    creds = None
    # token.json stores the user's access and refresh tokens.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run.
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    service = build('calendar', 'v3', credentials=creds)
    return service

def get_upcoming_events(service, query, max_results=5):
    """Retrieve the next n upcoming events from the primary calendar."""
    # Extract time range
    days = get_days_range_from_query(query)
    print(f'DAYS RECEIVED: {days}')
    if days == 0:
        days = 365
    now = datetime.now()
    future = now + timedelta(days=days)

    events_result = service.events().list(
        calendarId='primary',
        timeMin=now.isoformat() + 'Z',
        timeMax=future.isoformat() + 'Z',
        maxResults=max_results,
        singleEvents=True,
        orderBy='startTime'
    ).execute()

    events = events_result.get('items', [])

    if not events:
        print(f"You have no events in the next {days} day{'s' if days > 1 else ''}.")
        return f"You have no events in the next {days} day{'s' if days > 1 else ''}."

    lines = []
    for event in events:
        start_raw = event['start'].get('dateTime', event['start'].get('date'))
        # Convert ISO datetime to readable local time string
        try:
            dt_obj = datetime.datetime.fromisoformat(start_raw.replace('Z', '+00:00'))
            start_str = dt_obj.strftime("%A, %B %d at %-I:%M %p")
        except Exception:
            start_str = start_raw  # fallback
        summary = event.get('summary', 'No title')
        lines.append(f"- {summary} on {start_str}")
    x = "\n".join(lines)
    print(x)
    return x

def create_event(service, summary, start_datetime, end_datetime, timezone='UTC'):
    """Create a new event on the primary calendar.
    
    Parameters:
      - summary: Title for the event.
      - start_datetime and end_datetime: ISO formatted date strings.
      - timezone: Timezone of the event (default is 'UTC').
    """
    event_body = {
        'summary': summary,
        'start': {'dateTime': start_datetime, 'timeZone': timezone},
        'end': {'dateTime': end_datetime, 'timeZone': timezone},
    }
    event = service.events().insert(calendarId='primary', body=event_body).execute()
    return f"Event created: {event.get('htmlLink')}"
