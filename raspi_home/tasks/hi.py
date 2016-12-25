#!/usr/bin/env python

import re

from raspi_home.task import Task


class HiTask(Task):
    'Respond to message which contains "hi".'
    def match(self, channel, text, message):
        return re.search(re.compile('hi', re.IGNORECASE), text)

    def invoke(self, channel, text, message):
        message.reply('Hi from bot!')
