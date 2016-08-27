#!/usr/bin/env python
# -*- coding: utf-8 -*-

from slackbot.bot import respond_to, listen_to
import re
from raspi_server.say import say

@listen_to('.*', re.IGNORECASE)
def speach_weather(message):
    if message.channel._body['name'] == 'iot_weather':
        say("雨が振りそうです。洗濯物をたたんでください")
        message.reply("Spoken")
