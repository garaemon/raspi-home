#!/usr/bin/env python
"""
Speach message posted in iot_speach channel
"""

from raspi_server.say import say
from raspi_server.task import Task


class SpeachTask(Task):
    "Speach message posted in iot_speach channel"
    def match(self, channel, text, message):
        return channel == "iot_speach"

    def invoke(self, channel, text, message):
        say(text)
