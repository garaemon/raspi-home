#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
run raspi home server
"""

import os
import sys
import logging
from socket import gethostname

import coloredlogs

# first, add ../ to PYTHONPATH to import raspi_home
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import coloredlogs

from raspi_home.bot import Bot
from raspi_home.dispatcher import Dispatcher
from raspi_home.slackbot_patch import apply_patches
from raspi_home.tasks.hi import HiTask
from raspi_home.tasks.speach import SpeachTask
from raspi_home.tasks.weather import WeatherTask
from raspi_home.tasks.youtube_audio import YoutubeAudioTask
from raspi_home.utils.logger import SlackHandler, init_logging


def main():
    "main function"
    # setup logging
    log_format = init_logging()
    dispatcher = Dispatcher()
    dispatcher.registerTasks([HiTask(), SpeachTask(),
                              WeatherTask(), YoutubeAudioTask()])
    bot = Bot()
    root_logger = logging.getLogger()
    slack_log_handler = SlackHandler(bot, "iot_log")
    formatter = logging.Formatter(log_format)
    slack_log_handler.setFormatter(formatter)
    root_logger.addHandler(slack_log_handler)
    apply_patches(bot)
    bot.run()
    logging.info("booted")
    # say("サーバーを立ち上げました")
    bot.loop()

if __name__ == '__main__':
    # check os.environ
    if "SLACKBOT_API_TOKEN" not in os.environ:
        raise Exception("You should specify SLACKBOT_API_TOKEN")
    main()
