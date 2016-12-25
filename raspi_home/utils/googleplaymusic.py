#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Utilities for google play music
'''

from argparse import ArgumentParser
import logging                  # noqa: I100
import os                       # noqa: I100
import sys                      # noqa: I100
from types import MethodType    # noqa: I100

import gmusicapi.clients.musicmanager  # noqa: F401
from gmusicapi import Musicmanager
import gmusicapi.session as session

import httplib2  # included with oauth2client

import oauth2client

from raspi_home.utils.logger import init_logging

OAUTH_PATH = os.path.expanduser('~/.config/raspi_home/gmusicapi.cred')


# Applying patch
def patched_musicmanaer_login(self, oauth_credentials, *args, **kwargs):
    'Store an already-acquired oauth2client.Credentials.'
    super(session.Musicmanager, self).login()

    try:
        # refresh the token right away to check auth validity
        oauth_credentials.refresh(httplib2.Http(
            disable_ssl_certificate_validation=True))
    except oauth2client.client.Error:
        logging.exception('error when refreshing oauth credentials')

    if oauth_credentials.access_token_expired:
        logging.info('could not refresh oauth credentials')
        return False

    self._oauth_creds = oauth_credentials
    self.is_authenticated = True

    return self.is_authenticated


class GMClient(object):
    'Wrapper class of gmusicapi.Mobileclient'

    def __init__(self):
        # Aplying patch to session.Musicmanager
        session.Musicmanager.login = MethodType(patched_musicmanaer_login, None,
                                                session.Musicmanager)
        self.man = Musicmanager(verify_ssl=False)

        self.all_songs = None

    def login(self):
        if not os.path.exists(OAUTH_PATH):
            logging.error('No {} exists'.format(OAUTH_PATH))
            raise Exception('No {} exists'.format(OAUTH_PATH))
        else:
            self.man.login(oauth_credentials=OAUTH_PATH, uploader_name='raspi_home')
            logging.info('Success!')

        # These are required to change meta data.
        # raspi_home does not require it.
        # if ('GOOGLE_PLAY_MUSIC_PASS' in os.environ and
        #     'GOOGLE_PLAY_MUSIC_USER' in os.environ):
        #     self.api = Mobileclient()
        #     self.api.login(os.environ['GOOGLE_PLAY_MUSIC_USER'],
        #                    os.environ['GOOGLE_PLAY_MUSIC_PASS'],
        #                    Mobileclient.FROM_MAC_ADDRESS)
        #     logging.info('Logged in to google music')
        #     self.is_available = True
        # else:
        #     logging.warn('environmental variable GOOGLE_PLAY_MUSIC_PASS or GOOGLE_PLAY_MUSIC_USER'
        #                  ' is not available')
        #     self.api = None

    def oauth(self):
        'Run oauth for uploading/downloading songs'
        oauth_dir = os.path.dirname(OAUTH_PATH)
        if not os.path.exists(oauth_dir):
            logging.info('No oauth directory, create it')
            os.makedirs(oauth_dir)
        self.man.perform_oauth(open_browser=False, storage_filepath=OAUTH_PATH)

    # methods communicating with google server
    def update_songs(self):
        # if self.api is not None:
        #     self.all_songs = self.api.get_all_songs()
        # else:
        #     self.all_songs = []
        self.all_songs = self.man.get_uploaded_songs()

    def get_all_songs(self):
        if self.all_songs is None:
            self.update_songs()
        return self.all_songs

    def get_songs(self, artist=None):
        return [song for song in self.get_all_songs() if song['artist'] == artist]

    def upload(self, file):
        if not os.path.exists(file):
            logging.error('No {} exists'.format(file))
        else:
            (uploaded, matched, not_uploaded) = self.man.upload([file], enable_matching=True)
            if not_uploaded:
                logging.error('not uploaded because {}'.format(not_uploaded))

    def has_song(self, title):
        return title in [song['title'] for song in self.get_all_songs()]


def get_cli_argparser():
    'return argparse.ArgumentParser for cli usage'
    parser = ArgumentParser(description='cli interface for googleplaymusic')
    parser.add_argument('command', type=str, help='command to run', default='help')
    parser.add_argument('--file', '-f', type=str, help='mp3 file to upload')
    return parser


def run_cli_main():
    init_logging()
    parser = get_cli_argparser()
    args = parser.parse_args()
    logging.info('command ... {}'.format(args.command))
    if args.command == 'authorize':
        client = GMClient()
        client.oauth()
    elif args.command == 'test':
        # test credinental
        client = GMClient()
        client.login()
    elif args.command == 'upload':
        if args.file is None:
            logging.error('Please specify --file')
            sys.exit(1)
        upload_file = args.file
        client = GMClient()
        client.login()
        client.upload(upload_file)
    else:
        parser.print_help()
        sys.exit(0)


if __name__ == '__main__':
    run_cli_main()
