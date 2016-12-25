#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Task class to wrap callback function according to
slack message.
'''

from .utils.exceptions import MethodNotImplemented  # noqa: H304


class Task(object):
    def match(self, channel, text, message):
        raise MethodNotImplemented('Task.match is not implemented yet')

    def invoke(self, channel, text, message):
        raise MethodNotImplemented('Task.invoke is not implemented yet')
