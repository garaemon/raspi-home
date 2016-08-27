from slackbot.bot import respond_to, listen_to
import re

@respond_to('hi', re.IGNORECASE)
def cheer(message):
    print message
    print dir(message)
    message.reply('Hi!')

@listen_to('hi$', re.IGNORECASE)
def cheer(message):
    print message
    print dir(message)
    print dir(message.channel)
    print message.channel._body['name']
    message.reply('Hi to #{}!'.format(message.channel._body['name']))

