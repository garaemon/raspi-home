#!/usr/bin/env python

'''
Logger to broadcast message to slack.
'''

import logging


class SlackHandler(logging.Handler):
    """
    Custom logging handler to output log message to slack.
    """

    def __init__(self, bot, log_channel):
        self.bot = bot
        self.log_channel = log_channel
        super(SlackHandler, self).__init__()

    def emit(self, record):
        if self.bot and self.log_channel:
            try:
                self.bot.send_message_to_wo_logging(self.log_channel, self.format(record))
            except Exception:
                pass
