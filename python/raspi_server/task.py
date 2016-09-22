#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Task class to wrap callback function according to
slack message.
"""

from raspi_server.utils.exceptions import MethodNotImplemented


class Task:
    def match(self, channel, text, message):
        raise MethodNotImplemented("Task.match is not implemented yet")

    def invoke(self, channel, text, message):
        raise MethodNotImplemented("Task.invoke is not implemented yet")
