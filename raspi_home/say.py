#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Utility function for text-to-speach.
Other codes can use 'say' function for text-to-speach.
"""
# say

import subprocess
from sys import platform


def jtalk_linux(text, block=False):
    '''
    speach text with open_jtalk and aplay on linux.
    In fact, we expect Ubuntu.
'''
    open_jtalk = ['open_jtalk']
    mech = ['-x', '/var/lib/mecab/dic/open-jtalk/naist-jdic']
    htsvoice = ['-m', '/usr/share/hts-voice/mei/mei_normal.htsvoice']
    speed = ['-r', '1.0']
    outwav = ['-ow', 'open_jtalk.wav']
    cmd = open_jtalk + mech + htsvoice + speed + outwav
    jtalk_process = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    jtalk_process.stdin.write(text.encode('utf-8'))
    jtalk_process.stdin.close()
    jtalk_process.wait()
    aplay = ['aplay', '-q', 'open_jtalk.wav']
    aplay_process = subprocess.Popen(aplay)
    if block:
        aplay_process.wait()


def say_darwin(message, block=False):
    "speach text with say command on darwin."
    say_process = subprocess.Popen(["say", message])
    if block:
        say_process.wait()


def say(message, block=False):
    "speach-to-text function."
    if platform == "linux" or platform == "linux2":
        jtalk_linux(message, block)
    elif platform == "darwin":
        say_darwin(message, block)


if __name__ == '__main__':
    say("これはテストです", block=True)
