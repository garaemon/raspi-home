#!/usr/bin/env python
# -*- coding: utf-8 -*-

from slackbot.bot import respond_to, listen_to
import re
from raspi_server.say import say

@listen_to('.*', re.IGNORECASE)
def all_message_dispatch(message):
    if message.channel._body['name'] == 'iot_speach':
        say(message._body['text'])
    elif message.channel._body['name'] == 'iot_weather':
        say("雨が振りそうです。洗濯物をたたんでください")
        message.reply("Spoken")

