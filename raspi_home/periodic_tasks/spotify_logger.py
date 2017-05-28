#!/usr/bin/env python

from datetime import timedelta
import os
from time import sleep

from raspi_home.periodic_task import PeriodicTask
from raspi_home.utils.logger import init_logging

from raspi_home.utils.googlespreadsheet import Spreadsheet
from raspi_home.utils.spotify import SpotifyClient


class SpotifyLoggerTask(PeriodicTask):
    DEFAULT_INTERVAL = timedelta(minutes=60)

    def __init__(self, bot):
        PeriodicTask.__init__(self, self.DEFAULT_INTERVAL, bot, True)

    def execute(self):
        spotify_client = SpotifyClient()
        songs = spotify_client.get_recently_played()
        doc_id = os.environ['GOOGLE_SPREADSHEET_FOR_SPOTIFY']
        sheet = Spreadsheet(doc_id, 0)
        first_row = sheet.get_row()[0]
        if not first_row:
            first_row = '0'
        latest_timestamp = first_row
        for song in songs:
            timestamp = song.played_at
            print('timestamp: {}'.format(timestamp))
            print('latest_timestamp: {}'.format(latest_timestamp))
            if timestamp > latest_timestamp:
                sheet.insert_row(song.to_row())


if __name__ == '__main__':
    init_logging()
    task = SpotifyLoggerTask(None)
    while True:
        sleep(1)
