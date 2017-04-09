#!/usr/bin/env python
# coding: utf-8

'Utility class for radiko recording.'

import datetime
import logging
import os
import subprocess

import eyed3                    # noqa: I201

from raspi_home.utils.googleplaymusic import GMClient
from raspi_home.utils.logger import init_logging

REC_RADIKO_SCRIPT = os.path.join(os.path.dirname(__file__), '../../bin', 'rec_radiko.sh')


class RadikoRecorder(object):
    '''Class to record radiko.

    see http://www.dcc-jpl.com/foltia/wiki/radikomemo to know channel ID.
    '''
    def __init__(self, channel_id, duration_in_minutes, artist, album, upload_gmusic=True):
        self.channel_id = channel_id
        self.duration_in_minutes = duration_in_minutes
        self.artist = artist
        self.album = album
        self.upload_gmusic = upload_gmusic

    def run(self):
        'Start recording.'
        logging.info('Start recording {} for {} minutes'.format(self.channel_id,
                                                                self.duration_in_minutes))
        date_str = datetime.datetime.now().strftime('%Y-%m-%d-%H%M%S')
        output_filename = os.path.join('/tmp', '{}_{}.mp3'.format(date_str, self.channel_id))
        logging.info('save to {}'.format(output_filename))
        # This will block for self.duration_in_minutes.
        commands = [REC_RADIKO_SCRIPT, self.channel_id, str(int(self.duration_in_minutes)),
                    output_filename]
        logging.info('exec command: {}'.format(commands))
        subprocess.check_call(commands)
        if self.upload_gmusic:
            gmusic_client = GMClient()
            gmusic_client.login()
            title = u'{}-{}'.format(datetime.datetime.now().strftime('%Y-%m-%d'),
                                    self.album)
            # modify tag
            audiofile = eyed3.load(output_filename)
            audiofile.tag.artist = self.artist
            audiofile.tag.album = self.album
            audiofile.tag.title = title
            audiofile.tag.save()
            logging.info('Uploading recorded mp3 file')
            gmusic_client.upload(output_filename)
        logging.info('Remove recorded mp3 file')
        os.remove(output_filename)


if __name__ == '__main__':
    init_logging()
    job = RadikoRecorder('TBS', 1, u'test', u'test_album', True)
    job.run()
