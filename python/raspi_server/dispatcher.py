#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Dispatch according to received message.
Dispathcer class is a singleton class.
"""


class Dispatcher:
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "__instance__"):
            # store one object in __instance__ field to achieve
            # singleton class.
            cls.__instance__ = super(Dispatcher, object).__new__(cls, *args, **kwargs)
        return cls.__instance__

    def __init__(self):
        self.tasks = []

    def registerTask(self, task):
        self.tasks.append(task)

    def dispatch(self, message):
        for task in self.tasks:
            if task.match(message):
                task.invoke(message)
