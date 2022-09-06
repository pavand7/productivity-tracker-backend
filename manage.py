#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
from __future__ import print_function
# import httplib2
import os
import sys

# from apiclient import discovery
# Commented above import statement and replaced it below because of
# reader Vishnukumar's comment
# Src: https://stackoverflow.com/a/30811628
 
# import googleapiclient.discovery as discovery
# from oauth2client import client
# from oauth2client import tools
# from oauth2client.file import Storage

import datetime
from dateutil import tz

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
 
try:
    # import argparse
    from oauth2client import tools
    # flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
    flags = tools.argparser.parse_args([])
except ImportError:
    flags = None

events = []
# # If modifying these scopes, delete your previously saved credentials
# # at ~/.credentials/calendar-python-quickstart.json
# SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
# CLIENT_SECRET_FILE = 'client_secret_google_calendar.json'
# APPLICATION_NAME = 'Google Calendar API'

# def get_credentials():
#     """Gets valid user credentials from storage.
 
#     If nothing has been stored, or if the stored credentials are invalid,
#     the OAuth2 flow is completed to obtain the new credentials.
 
#     Returns:
#         Credentials, the obtained credential.
#     """
#     home_dir = os.path.expanduser('./backend')
#     credential_dir = os.path.join(home_dir, '.credentials')
#     # if not os.path.exists(credential_dir):
#     #     os.makedirs(credential_dir)
#     credential_path = os.path.join(credential_dir,
#                                    'client_secret_google_calendar.json')
 
#     store = Storage(credential_path)
#     credentials = store.get()
#     if not credentials or credentials.invalid:
#         flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
#         flow.user_agent = APPLICATION_NAME
#         if flags:
#             credentials = tools.run_flow(flow, store, flags)
#         else:  # Needed only for compatibility with Python 2.6
#             credentials = tools.run(flow, store)
#         print('Storing credentials to ' + credential_path)
#     return credentials

# def calendar():
#     """Shows basic usage of the Google Calendar API.
 
#     Creates a Google Calendar API service object and outputs a list of the next
#     10 events on the user's calendar.
#     """
#     credentials = get_credentials()
#     http = credentials.authorize(httplib2.Http())
#     service = discovery.build('calendar', 'v3', http=http)
 
#     # This code is to fetch the calendar ids shared with me
#     # Src: https://developers.google.com/google-apps/calendar/v3/reference/calendarList/list
#     page_token = None
#     calendar_ids = []
#     while True:
#         calendar_list = service.calendarList().list(pageToken=page_token).execute()
#         for calendar_list_entry in calendar_list['items']:
#             if '@qxf2.com' in calendar_list_entry['id']:
#                 calendar_ids.append(calendar_list_entry['id'])
#         page_token = calendar_list.get('nextPageToken')
#         if not page_token:
#             break
 
#     # This code is to look for all-day events in each calendar for the month of September
#     # Src: https://developers.google.com/google-apps/calendar/v3/reference/events/list
#     # You need to get this from command line
#     # Bother about it later!
#     start_date = datetime.datetime(2022, 9, 6, 00, 00, 00, 0).isoformat() + 'Z'
#     end_date = datetime.datetime(2022, 9, 6, 23, 59, 59, 0).isoformat() + 'Z'
 
#     for calendar_id in calendar_ids:
#         count = 0
#         print('\n----%s:\n' % calendar_id)
#         eventsResult = service.events().list(
#             calendarId=calendar_id,
#             timeMin=start_date,
#             timeMax=end_date,
#             singleEvents=True,
#             orderBy='startTime').execute()
#         events = eventsResult.get('items', [])
#         if not events:
#             print('No upcoming events found.')
#         for event in events:
#             if event.has_key('summary'):
#                 if 'PTO' in event['summary']:
#                     count += 1
#                     start = event['start'].get(
#                         'dateTime', event['start'].get('date'))
#                     print(start, event['summary'])
#         print('Total days off for %s is %d' % (calendar_id, count))

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']


def calendar():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                './client_secret_new.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('calendar', 'v3', credentials=creds)

        # Call the Calendar API
        today = datetime.datetime.utcnow().date()
        start_date = datetime.datetime(today.year, today.month, today.day, 00, 00, 00, 0).isoformat() + 'Z'
        end_date = datetime.datetime(today.year, today.month, today.day, 23, 59, 59, 0).isoformat() + 'Z'
        print("Getting today's events")
        events_result = service.events().list(calendarId='primary', timeMin=start_date,
                                              timeMax=end_date, singleEvents=True,
                                              orderBy='startTime').execute()
        events = events_result.get('items', [])

        if not events:
            print('No events found today.')
            return

        # Prints the start and name of the next 10 events
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            print(start, event['summary'])

    except HttpError as error:
        print('An error occurred: %s' % error)

def main():

    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    calendar()
    main()