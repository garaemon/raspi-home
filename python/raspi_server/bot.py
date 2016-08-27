"""
Provide Bot class to wrap slackbot.bot.Bot class with better interface.
"""
# Wrapper of slackbot.bot.Bot
import slackbot.bot
from six.moves import _thread


class Bot(slackbot.bot.Bot):
    "Wrapper class of slackbot.bot.Bot"
    def run(self):
        "It does not run main loop, just initialization"
        self._plugins.init_plugins()
        self._dispatcher.start()
        self._client.rtm_connect()
        _thread.start_new_thread(self._keepactive, tuple())

    def get_client(self):
        "return instance of slackbot.slackclient.SlackClient"
        return self._client

    def get_channel(self, name):
        "return body of channel"
        return self.get_client().find_channel_by_name(name)

    def send_message_to(self, channel, message):
        "send message to specified channel"
        self.get_client().rtm_send_message(self.get_channel(channel),
                                           message)

    def loop(self):
        "run main loop with dispatcher"
        self._dispatcher.loop()
