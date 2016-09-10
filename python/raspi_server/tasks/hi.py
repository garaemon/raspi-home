#!/usr/bin/env python

from raspi_server.task import Task
import re


class HiTask(Task):
    "Respond to message which contains 'hi'."
    def match(self, channel, text, message):
        return re.search(re.compile('hi', re.IGNORECASE), text)

    def invoke(self, channel, text, message):
        message.reply('Hi from bot!')
