#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Speach when wheather goes to rain
"""

from raspi_server.say import say
from raspi_server.task import Task


class WeatherTask(Task):
    "Speach when something is posted on iot_weather channel"
    def match(self, channel, text, message):
        return channel == "iot_weather"

    def invoke(self, channel, text, message):
        say("雨が振りそうです。洗濯物をとりこんで")
        message.reply("Spoken")
