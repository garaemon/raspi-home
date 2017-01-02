#!/usr/bin/env python
'''
Logger to broadcast message to slack.
'''

import logging
from socket import gethostname

import coloredlogs


class SlackHandler(logging.Handler):
    'Custom logging handler to output log message to slack.'

    def __init__(self, bot, log_channel):
        self.bot = bot
        self.log_channel = log_channel
        super(SlackHandler, self).__init__()

    def emit(self, record):
        if self.bot and self.log_channel:
            try:
                self.bot.send_message_to_wo_logging(self.log_channel, self.format(record))
            except Exception as e:
                print('slack Exception: {}'.format(e))


def init_logging():
    'Function to initialize logger.'
    field_styles = coloredlogs.DEFAULT_FIELD_STYLES
    field_styles['levelname'] = {'color': 'white', 'bold': True}
    log_format = '%(asctime)s {} [%(levelname)s] [%(filename)s:%(lineno)d] %(message)s'.format(
        gethostname())
    coloredlogs.install(level=logging.INFO,
                        fmt=log_format,
                        field_styles=field_styles)
    return log_format
