#!/usr/bin/env python

'''Provide PeriodicTask class to run specified task periodically.'''

from datetime import timedelta
import logging
from threading import Thread
from time import sleep

from raspi_home.utils.exceptions import MethodNotImplemented
from raspi_home.utils.logger import init_logging


class PeriodicTask(Thread):
    'Super class for periodical tasks.'
    def __init__(self, interval_timedelta, bot, start_when_created=True):
        self.interval = interval_timedelta
        self.bot = bot
        Thread.__init__(self)
        self.daemon = True
        if start_when_created:
            self.start()

    def execute(self):
        '''Method to be invoked with specified interval.

        This method should be implemented in subclass of PeriodicTask.
        Otherwise, MethodNotImplemented exception is raised.
        '''
        raise MethodNotImplemented('execute method should be implemented in subclass'
                                   ' of PeriodicTask')

    def run(self):
        '''Threading function.

        run method calls execute with sleeping for self.interval seconds.
        '''
        while True:
            self.execute()
            sleep(self.interval.total_seconds())


class SamplePeriodicHello(PeriodicTask):
    'Sample task for demonstration'
    def execute(self):
        logging.info('Hello from execute method')


if __name__ == '__main__':
    init_logging()
    hello_task = SamplePeriodicHello(timedelta(seconds=2), None)
    while True:
        sleep(1)
