#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Dispatch according to received message.
Dispathcer class is a singleton class.
'''

import logging


class Dispatcher(object):
    def __new__(cls, *args, **kwargs):
        logging.debug('Dispatcher.__new__ is called')
        if not hasattr(cls, '__instance__'):
            # store one object in __instance__ field to achieve
            # singleton class.
            cls.__instance__ = super(Dispatcher, cls).__new__(cls, *args, **kwargs)
        return cls.__instance__

    def __init__(self):
        logging.debug('Dispatcher.__init__ is called')
        if not hasattr(self, 'tasks'):
            self.tasks = []

    def registerTask(self, task):
        logging.debug('Register a task: {}'.format(task))
        self.tasks.append(task)

    def registerTasks(self, tasks):
        for t in tasks:
            self.registerTask(t)

    def dispatch(self, message):
        logging.debug('Dispatch!')
        channel = message.channel._body['name']
        try:
            text = message.body['attachments'][0]['text']
        except Exception:
            text = message.body['text']
        for task in self.tasks:
            if task.match(channel, text, message):
                task.invoke(channel, text, message)
