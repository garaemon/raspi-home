#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Speach when wheather goes to rain
"""

from raspi_home.say import say
from raspi_home.task import Task


class WeatherTask(Task):
    "Speach when something is posted on iot_weather channel"
    def match(self, channel, text, message):
        return channel == "iot_weather"

    def invoke(self, channel, text, message):
        say(u"雨が振りそうです。洗濯物をとりこんでください")
        message.reply("Spoken")
