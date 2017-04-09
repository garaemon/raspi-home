#!/usr/bin/env python

from __future__ import print_function

import argparse
import datetime
import json
import logging
import os

from apiclient import discovery
import httplib2
from oauth2client import client
from oauth2client.file import Storage
from oauth2client import tools

from raspi_home.utils.logger import init_logging

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/calendar-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
CLIENT_SECRET_FILE = os.path.expanduser('~/.raspi-home-secrets/google_calendar_client_id.json')
APPLICATION_NAME = 'raspi_home'


def get_credentials():
    '''Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    '''
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.raspi-home-secrets/')
    credential_path = os.path.join(credential_dir,
                                   'calendar-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if credentials:
        logging.info('You already have credentials')
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
        credentials = tools.run_flow(flow, store, flags)
        logging.info('Storing credentials to ' + credential_path)
    return credentials


def verify_client_id():
    'Verify there is client_id.json in ~/.raspi-home-secrets/ directory.'
    if os.path.exists(CLIENT_SECRET_FILE):
        logging.info('Found client secret file at {}'.format(CLIENT_SECRET_FILE))
        return True
    else:
        raise Exception('No client secret file at {}'.format(CLIENT_SECRET_FILE))


class GCalClient(object):
    'Wrapper of google calendar api'

    def __init__(self, calendar_name, calendar_id):
        self.credentials = get_credentials()

        self.calendar_name = calendar_name
        self.calendar_id = calendar_id

    def build_service(self):
        http = self.credentials.authorize(httplib2.Http())
        return discovery.build('calendar', 'v3', http=http)

    def get_upcoming_events(self, num):
        now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
        service = self.build_service()
        events_result = service.events().list(
            calendarId=self.calendar_id, timeMin=now, maxResults=num, singleEvents=True,
            orderBy='startTime').execute()
        return events_result.get('items', [])


if __name__ == '__main__':
    init_logging()
    verify_client_id()
    get_credentials()
    gcalclient = GCalClient('Radio', 'a40uhlmikgmbd0h5l8s5hhcku0@group.calendar.google.com')
    for event in gcalclient.get_upcoming_events(1):
        print(event)
        print('{} @ {} ({} -- {})'.format(event['summary'],
                                          event['location'],
                                          event['start']['dateTime'], event['end']['dateTime']))
        print('-- {}'.format(event['description']))
        desc = json.loads(event['description'])
        print('-- artist: {}'.format(desc['artist']))
        print('-- album: {}'.format(desc['album']))
