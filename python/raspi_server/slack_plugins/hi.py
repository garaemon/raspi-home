"""
slackbot plugin to respond against 'Hi'.
It is used for debugging.
"""
import re
from slackbot.bot import respond_to, listen_to


@respond_to('hi', re.IGNORECASE)
def cheer_respond_to(message):
    "callback function for 'hi' reply"
    print message
    print dir(message)
    message.reply('Hi!')


@listen_to('hi$', re.IGNORECASE)
def cheer_listen_to(message):
    "callback function for 'hi' message."
    print message
    print dir(message)
    print dir(message.channel)
    print message.channel._body['name']
    message.reply('Hi to #{}!'.format(message.channel._body['name']))
