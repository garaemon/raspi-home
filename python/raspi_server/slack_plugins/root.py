#!/usr/bin/env python
# -*- coding: utf-8 -*-
"Root dispatcher for received message."

import re
from slackbot.bot import listen_to

from raspi_server.say import say


@listen_to('.*', re.IGNORECASE)
def all_message_dispatch(message):
    "dispatch according to any received messages"
    if message.channel._body['name'] == 'iot_speach':
        say(message._body['text'])
    elif message.channel._body['name'] == 'iot_weather':
        say("雨が振りそうです。洗濯物をたたんでください")
        message.reply("Spoken")
