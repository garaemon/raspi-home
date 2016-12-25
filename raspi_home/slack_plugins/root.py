#!/usr/bin/env python
# -*- coding: utf-8 -*-
'Root dispatcher for received message.'

import re

from slackbot.bot import listen_to

from raspi_home.dispatcher import Dispatcher  # noqa: I100


@listen_to('.*', re.IGNORECASE)
def all_message_dispatch(message):
    'dispatch according to any received messages'
    dispatcher = Dispatcher()
    dispatcher.dispatch(message)
    # if message.channel._body['name'] == 'iot_speach':
    #     say(message._body['text'].encode('utf-8'))
    # elif message.channel._body['name'] == 'iot_weather':
    #     say('雨が振りそうです。洗濯物をたたんでください')
    #     message.reply('Spoken')
