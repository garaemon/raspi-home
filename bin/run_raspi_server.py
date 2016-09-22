#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
run raspi home server
"""

import os

from raspi_home.bot import Bot
from raspi_home.slackbot_patch import apply_patches
from raspi_home.dispatcher import Dispatcher
from raspi_home.tasks.hi import HiTask
from raspi_home.tasks.speach import SpeachTask
from raspi_home.tasks.weather import WeatherTask
from raspi_home.tasks.youtube_audio import YoutubeAudioTask


def main():
    "main function"
    dispatcher = Dispatcher()
    dispatcher.registerTasks([HiTask(), SpeachTask(),
                              WeatherTask(), YoutubeAudioTask()])
    bot = Bot()
    apply_patches(bot)
    bot.run()
    bot.send_message_to("iot_log", "booted")
    # say("サーバーを立ち上げました")
    bot.loop()

if __name__ == '__main__':
    # check os.environ
    if "SLACKBOT_API_TOKEN" not in os.environ:
        raise Exception("You should specify SLACKBOT_API_TOKEN")
    main()
