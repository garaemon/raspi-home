#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Task class to wrap callback function according to
slack message.
"""

from utils.exceptions import MethodNotImplemented

class Task:
    def __init__(self, name):
        self.name = name

    def match(self, message):
        raise MethodNotImplemented

    def invoke(self, message):
        pass
