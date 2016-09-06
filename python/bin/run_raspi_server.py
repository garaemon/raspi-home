#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
run raspi home server
"""

import os

from raspi_server.bot import Bot
# from raspi_server.say import say


def main():
    "main function"
    bot = Bot()
    bot.run()
    bot.send_message_to("iot_channel", "booted")
    # say("サーバーを立ち上げました")
    bot.loop()

if __name__ == '__main__':
    # check os.environ
    if "SLACKBOT_API_TOKEN" not in os.environ:
        raise Exception("You should specify SLACKBOT_API_TOKEN")
    main()
