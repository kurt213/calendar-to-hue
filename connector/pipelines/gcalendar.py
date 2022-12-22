if __name__ == '__main__' and __package__ is None:
    import sys
    from os import path
    sys.path.append( path.dirname( path.dirname (path.dirname( path.abspath(__file__) ) ) ))

from datetime import datetime, timedelta
import pickle
import os.path
import inspect
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

from connector.access import secrets

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']


class CalendarAccess:

    def __init__(self):

        access_name = 'credentials.json'
        access_path = os.path.dirname(inspect.getfile(secrets))
        access_json = os.path.join(access_path, access_name)

        creds = None

        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    access_json, SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        self.service = build('calendar', 'v3', credentials=creds)

    def get_today_events(self):
        """ Get today's confirmed events

        Get today's calendar events to add into schedule
        
        """

        # Call the Calendar API
        today = datetime.utcnow().date()
        tomorrow = today + timedelta(1)
        start = datetime(today.year, today.month, today.day, 0, 0).isoformat() + 'Z'
        end = datetime(tomorrow.year, tomorrow.month, tomorrow.day, 0, 0).isoformat() + 'Z'
        print("Getting today's events")

        events_result = self.service.events().list(calendarId='primary', timeMin=start, timeMax=end,
                                            maxResults=10, singleEvents=True,
                                            orderBy='startTime').execute()
        events = events_result.get('items', [])

        if not events:
            print('No events for today found.')
        
        event_list = []
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            end = event['end'].get('dateTime', event['end'].get('date'))
            #start_convert = datetime.strptime(start, '%Y-%m-%dT%H:%M:%S%z')
            #print(start_convert)
            event_list.append({
                'start_time': start,
                'end_time': end,
                'event_name': event['summary'],
                'status': event['status']
            })

        return event_list

if __name__ == '__main__':
    
    gcalendar = CalendarAccess()
    events = gcalendar.get_today_events()
    print(events)
