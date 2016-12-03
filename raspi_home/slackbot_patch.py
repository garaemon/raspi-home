#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Apply patch to skypebot:
- Allow message by bot
"""

from slackbot.dispatcher import Message, MessageDispatcher
import logging
import traceback

logger = logging.getLogger(__name__)


def on_new_message_allow_bot_message(self, msg):
    # ignore edits
    subtype = msg.get('subtype', '')
    if subtype == u'message_changed':
        return
    botname = self._client.login_data['self']['name']
    try:
        msguser = self._client.users.get(msg['user'])
        username = msguser['name']
        if username == botname:
            return
    except (KeyError, TypeError):
        if 'username' in msg:
            username = msg['username']
        else:
            return

    if username == u'slackbot':
        return

    msg_respond_to = self.filter_text(msg)
    if msg_respond_to:
        self._pool.add_task(('respond_to', msg_respond_to))
    else:
        self._pool.add_task(('listen_to', msg))


def dispatch_msg_handler_with_bot_message(self, category, msg):
    responded = False
    if 'text' in msg:
        text = msg['text']
    else:
        text = msg['attachments'][0]['text']
    for func, args in self._plugins.get_plugins(category, text):
        if func:
            responded = True
            try:
                func(Message(self._client, msg), *args)
            except Exception:
                logger.exception(
                    'failed to handle message %s with plugin "%s"',
                    text, func.__name__)
                reply = u'[{}] I had a problem handling "{}"\n'.format(
                    func.__name__, text)
                tb = u'```\n{}\n```'.format(traceback.format_exc())
                if self._errors_to:
                    self._client.rtm_send_message(msg['channel'], reply)
                    self._client.rtm_send_message(self._errors_to,
                                                  u'{}\n{}'.format(reply,
                                                                  tb))
                else:
                    self._client.rtm_send_message(msg['channel'],
                                                  u'{}\n{}'.format(reply,
                                                                  tb))
    return responded


def apply_patches(bot):
    on_new_message_function_type = type(MessageDispatcher._on_new_message)
    bot._dispatcher._on_new_message \
        = on_new_message_function_type(on_new_message_allow_bot_message,
                                       bot._dispatcher, MessageDispatcher)
    dispatch_msg_function_type = type(MessageDispatcher._dispatch_msg_handler)
    bot._dispatcher._dispatch_msg_handler \
        = dispatch_msg_function_type(dispatch_msg_handler_with_bot_message,
                                     bot._dispatcher, MessageDispatcher)
