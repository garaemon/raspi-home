#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Convert youtube movie to mp3
'''
from __future__ import unicode_literals

import datetime
import json
import logging
import os
import threading

import coloredlogs              # noqa: I201
import eyed3                    # noqa: I201
import youtube_dl               # noqa: I201

from raspi_home.task import Task
from raspi_home.utils.googleplaymusic import GMClient


def message_safe_reply(message, msg):
    try:
        message.reply(msg)
    except Exception:
        pass


class TargetData(object):
    BASE_OUTPUT_NAME = 'downloaded_file'
    SUFFIX = 'mp3'

    def __init__(self, text):
        json_obj = json.loads(text)
        # url may wrapped with '<>'.
        self.url = json_obj['url']
        if self.url.startswith('<'):
            self.url = self.url[1:]
        if self.url.endswith('>'):
            self.url = self.url[:-1]
        self.artist = json_obj['artist']
        self.album = json_obj['album']

    def copy_with_url(self, new_url):
        '''Create new TargetData with different url.

        Other filds are copied to new TargetData instnace.
        '''
        new_args = {
            'url': new_url,
            'artist': self.artist,
            'album': self.album}

        return TargetData(json.dumps(new_args))

    def is_youtube_list(self, info):
        'Check if info is youtube video list or not.'
        return '_type' in info and info['_type'] == 'playlist'

    def download(self, message, upload=True, songs=None):
        date_str = datetime.datetime.now().strftime('%y%m%d_%H%M%S')
        output_filename = os.path.join('/tmp', '_'.join([self.BASE_OUTPUT_NAME, date_str]))
        ydl_opts = {'audioformat': 'mp3', 'format': 'bestaudio/best',
                    'outtmpl': '{}.%(ext)s'.format(output_filename),
                    'quiet': True,
                    'nocheckcertificate': True,
                    'ignoreerrors': True,
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '5',
                        'nopostoverwrites': False,
                    }]}
        logging.info('youtube url ==> ', self.url)
        if message:
            message_safe_reply(message, 'Received download request from {}'.format(self.url))
        if upload:
            logging.info('Logging in to gmusic')
            gmusic_client = GMClient()
            gmusic_client.login()
            if songs is None:
                songs = gmusic_client.get_all_songs()
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(self.url, download=False)
            if self.is_youtube_list(info):
                logging.info('Looks youtube list, download them as list')
                for entry in info['entries']:
                    try:
                        logging.info('entry url: {}'.format(entry['webpage_url']))
                        new_data = self.copy_with_url(entry['webpage_url'])
                        new_data.download(message, upload=upload, songs=songs)
                    except Exception as e:
                        logging.error('Failed to download: {}'.format(e))
                logging.info('Done processing all videos in the youtube list')
                return
            if upload:
                # check the song is already uploaded
                if info.get('title') in [song['title'] for song in songs]:
                    warn_message = u'{} is already uploaded. skip downloading'.format(
                        info.get('title'))
                    logging.warn(warn_message)
                    if message:
                        message_safe_reply(message, warn_message)
                    return
                else:
                    logging.info(u'{} is not uploaded yet'.format(
                        info.get('title')))
            logging.info('Download \'{}\' from \'{}\' to \'{}\''.format(
                info.get('url'),
                info.get('title'), output_filename))
            if message:
                message_safe_reply(message, 'Download \'{}\' from \'{}\' to \'{}\''.format(
                    info.get('url'),
                    info.get('title'), output_filename))
            ydl.download([self.url])
        output_filename_with_suffix = output_filename + '.mp3'
        if message:
            message_safe_reply(message, 'Done downloading to {}'.format(
                output_filename_with_suffix))
            message_safe_reply(message, 'Updating tag information')
        self.updateTagInformation(output_filename_with_suffix, info)
        if upload:
            if message:
                message_safe_reply(message, 'Start uploading')
            logging.info('Uploading to gmusic')
            gmusic_client.upload(output_filename_with_suffix)
            if message:
                message_safe_reply(message, 'Done uploading')
            logging.info('Done uploading')
        # remove donloaded file
        logging.info('Remove downloaded file: {}'.format(output_filename_with_suffix))
        try:
            os.remove(output_filename_with_suffix)
        except Exception as e:
            logging.error('Error during remove file: {}'.format(e))

    def updateTagInformation(self, filename, info):
        audiofile = eyed3.load(filename)
        audiofile.tag.artist = self.artist
        audiofile.tag.album = self.album
        audiofile.tag.title = info.get('title')
        audiofile.tag.save()


class YoutubeAudioTask(Task):
    def match(self, channel, text, message):
        text = text.replace(u'”', u'"').replace(u'“', u'"')  # fix closing double quotes
        if channel == 'iot_youtube_audio':
            try:
                # try to parse as json
                json_obj = json.loads(text)
                if 'url' in json_obj and 'artist' in json_obj and 'album' in json_obj:
                    return True
                else:
                    logging.error('It is not for youtube_audio json')
                    return False
            except Exception as e:
                logging.error('It is not json: {}'.format(e.message))
                return False
        else:
            return False

    def download_async(self, data, message):
        try:
            data.download(message, upload=True)
        except Exception as e:
            logging.error('failed to download: {}'.format(e))
            message_safe_reply(message, 'failed to download: {}'.format(e))

    def invoke(self, channel, text, message):
        text = text.replace(u'”', u'"').replace(u'“', u'"')  # fix closing double quotes
        data = TargetData(text)
        message_safe_reply(message, 'received message')
        thread = threading.Thread(target=self.download_async, args=(data, message))
        thread.start()
        return thread


def demo_onefile():
    logging.info('Running demo_onefile: download MJ and PM\'s say say say')
    test_data1 = TargetData(u'''
    {
      "url": "https://www.youtube.com/watch?v=Hq5KAdWJiWY",
      "artist": "Paul McCartney and Michael Jackson",
      "album": "test from youtube_audio.py"
    }
    ''')
    test_data1.download(None)


def demo_list():
    logging.info('Running demo_onefile: download video list')
    test_data1 = TargetData(u'''
    {
      "url": "https://www.youtube.com/user/akabane1981/videos",
      "artist": "Test Video List",
      "album": "test from youtube_audio.py"
    }
    ''')
    test_data1.download(None, upload=False)


if __name__ == '__main__':
    field_styles = coloredlogs.DEFAULT_FIELD_STYLES
    field_styles['levelname'] = {'color': 'white', 'bold': True}
    coloredlogs.install(level=logging.INFO,
                        fmt='%(asctime)s [%(levelname)s] %(message)s',
                        field_styles=field_styles)
    # demo_onefile()
    demo_list()
