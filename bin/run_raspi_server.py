#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
run raspi home server
"""

import logging
import os
import sys

# first, add ../ to PYTHONPATH to import raspi_home
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from raspi_home.bot import Bot  # noqa: E402
from raspi_home.dispatcher import Dispatcher  # noqa: E402
from raspi_home.periodic_tasks.gcal_radiko import GCalRadikoTask  # noqa: E402
from raspi_home.periodic_tasks.spotify_logger import SpotifyLoggerTask  # noqa: E402
from raspi_home.slackbot_patch import apply_patches  # noqa: E402
from raspi_home.tasks.hi import HiTask  # noqa: E402
from raspi_home.tasks.speach import SpeachTask  # noqa: E402
from raspi_home.tasks.weather import WeatherTask  # noqa: E402
from raspi_home.tasks.youtube_audio import YoutubeAudioTask  # noqa: E402
from raspi_home.utils.logger import init_logging  # noqa: E402
from raspi_home.utils.logger import SlackHandler  # noqa: E402


def main():
    "main function"
    # setup logging
    log_format = init_logging()
    dispatcher = Dispatcher()
    dispatcher.registerTasks([HiTask(), SpeachTask(),
                              WeatherTask(), YoutubeAudioTask()])
    bot = Bot()
    periodic_tasks = [GCalRadikoTask(bot), SpotifyLoggerTask(bot)]  # noqa: F841
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
