#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Convert youtube movie to mp3
"""
from __future__ import unicode_literals
import datetime
import json
import logging
import os
import threading

import coloredlogs

import eyed3
import youtube_dl

from raspi_home.task import Task
from raspi_home.utils.googleplaymusic import GMClient


class TargetData(object):
    BASE_OUTPUT_NAME = "downloaded_file"
    SUFFIX = "mp3"

    def __init__(self, text):
        json_obj = json.loads(text)
        # url may wrapped with '<>'.
        self.url = json_obj["url"]
        if self.url.startswith('<'):
            self.url = self.url[1:]
        if self.url.endswith('>'):
            self.url = self.url[:-1]
        self.artist = json_obj["artist"]
        self.album = json_obj["album"]

    def download(self, message, upload=True):
        date_str = datetime.datetime.now().strftime("%y%m%d_%H%M%S")
        output_filename = os.path.join('/tmp', "_".join([self.BASE_OUTPUT_NAME, date_str]))
        ydl_opts = {'audioformat': 'mp3', 'format': 'bestaudio/best',
                    'outtmpl': '{}.%(ext)s'.format(output_filename),
                    'quiet': True,
                    'nocheckcertificate': True,
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '5',
                        'nopostoverwrites': False,
                    }]}
        logging.info('youtube url ==> ', self.url)
        if message:
            message.reply("Received download request from {}".format(self.url))
        if upload:
            logging.info('Logging in to gmusic')
            gmusic_client = GMClient()
            gmusic_client.login()
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(self.url, download=False)
            if upload:
                # check the song is already uploaded
                if gmusic_client.has_song(info.get('title')):
                    warn_message = u"{} is already uploaded. skip downloading".format(
                        info.get('title'))
                    logging.warn(warn_message)
                    if message:
                        message.reply(warn_message)
                    return
                else:
                    logging.info(u"{} is not uploaded yet".format(
                        info.get('title')))
            logging.info('Download \'{}\' from \'{}\' to \'{}\''.format(
                info.get('url'),
                info.get('title'), output_filename))
            if message:
                message.reply('Download \'{}\' from \'{}\' to \'{}\''.format(
                    info.get('url'),
                    info.get('title'), output_filename))
            ydl.download([self.url])
        if message:
            message.reply("Done downloading to {}.mp3".format(output_filename))
            message.reply("Updating tag information")
        self.updateTagInformation(output_filename + '.mp3', info)
        if upload:
            if message:
                message.reply("Start uploading")
            logging.info('Uploading to gmusic')
            gmusic_client.upload(output_filename + '.mp3')
            if message:
                message.reply("Done uploading")
            logging.info("Done uploading")

    def updateTagInformation(self, filename, info):
        audiofile = eyed3.load(filename)
        audiofile.tag.artist = self.artist
        audiofile.tag.album = self.album
        audiofile.tag.title = info.get('title')
        audiofile.tag.save()


class YoutubeAudioTask(Task):
    def match(self, channel, text, message):
        text = text.replace(u'”', u'"').replace(u'“', u'"')  # fix closing double quotes
        logging.info("text: {}".format(text))
        if channel == "iot_youtube_audio":
            try:
                # try to parse as json
                json_obj = json.loads(text)
                if "url" in json_obj and "artist" in json_obj and "album" in json_obj:
                    return True
                else:
                    logging.error("It's not for youtube_audio json")
                    return False
            except Exception, e:
                logging.error("It's not json: {}".format(e.message))
                return False
        else:
            return False

    def download_async(self, data, message):
        try:
            data.download(message, upload=True)
        except Exception, e:
            message.reply("failed to download: {}".format(e.message))

    def invoke(self, channel, text, message):
        text = text.replace(u'”', u'"').replace(u'“', u'"')  # fix closing double quotes
        data = TargetData(text)
        message.reply("received message")
        thread = threading.Thread(target=self.download_async, args=(data, message))
        thread.start()
        return thread


def demo_onefile():
    logging.info("Running demo_onefile: download MJ and PM's say say say")
    test_data1 = TargetData(u'''
    {
      "url": "https://www.youtube.com/watch?v=Hq5KAdWJiWY",
      "artist": "Paul McCartney and Michael Jackson",
      "album": "test from youtube_audio.py"
    }
    ''')
    test_data1.download(None)

if __name__ == "__main__":
    field_styles = coloredlogs.DEFAULT_FIELD_STYLES
    field_styles['levelname'] = {'color': 'white', 'bold': True}
    coloredlogs.install(level=logging.INFO,
                        fmt='%(asctime)s [%(levelname)s] %(message)s',
                        field_styles=field_styles)
    demo_onefile()
