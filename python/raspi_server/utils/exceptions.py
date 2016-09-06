#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Provide exception classes used in raspi-home project.
"""

class RaspiHomeException(Exception):
    "Root exception class used in raspi-home project"
    pass

class MethodNotImplemented(RaspiHomeException):
    "Exception which is raised when unimplemented method is called"
    pass
