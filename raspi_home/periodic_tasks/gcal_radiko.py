#!/usr/bin/env python

from datetime import datetime
from datetime import timedelta
from dateutil.parser import parse
import json
import logging
from time import sleep
from tzlocal import get_localzone

from apscheduler.schedulers.background import BackgroundScheduler

from raspi_home.periodic_task import PeriodicTask
from raspi_home.utils.googlecalendar import GCalClient
from raspi_home.utils.logger import init_logging
from raspi_home.utils.radiko import RadikoRecorder


class GCalRadikoTask(PeriodicTask):
    '''Periodical task to query google calendar and record radiko at specified schedule.

    GCalRadikoTask expects to be created like GCalRadikoTask(GCalRadikoTask.DEFAULT_INTERVAL).
    '''
    DEFAULT_INTERVAL = timedelta(minutes=20)
    SCHEDULE_OFFSET = timedelta(minutes=2)
    NUM_EVENTS_TO_WATCH = 10
    _schedules = {}

    def __init__(self, bot):
        PeriodicTask.__init__(self, self.DEFAULT_INTERVAL, bot, True)

    def execute(self):
        'Query google calendar event and register radiko schedule if needed'
        events = self.get_upcoming_radiko_events()
        for event in events:
            if not self.is_event_scheduled(event):
                self.register_radiko_schedule(event)
        logging.info(u'current jobs are: {}'.format(self._schedules.keys()))

    def get_upcoming_radiko_events(self):
        'Query google calender and return upcoming event objects.'
        logging.info('Querying google calendar')
        gcalclient = GCalClient('Radio', 'a40uhlmikgmbd0h5l8s5hhcku0@group.calendar.google.com')
        events = gcalclient.get_upcoming_events(self.NUM_EVENTS_TO_WATCH)

        return events

    def is_event_scheduled(self, event):
        'Return true if event is already scheduled.'
        event_key = self.get_event_key(event)
        return event_key in self._schedules

    def get_event_key(self, event):
        'Create tuple from summary, start date and end date.'
        return (event['summary'], event['start']['dateTime'], event['end']['dateTime'])

    def register_radiko_schedule(self, event):
        'Register a new radiko job as schedule.'
        event_key = self.get_event_key(event)
        start_datetime = parse(event['start']['dateTime'])
        end_datetime = parse(event['end']['dateTime'])
        now = datetime.now(get_localzone())
        if now >= start_datetime:
            logging.info('{} is already started.'.format(event_key))
            return
        start_datetime_with_offset = start_datetime - self.SCHEDULE_OFFSET
        end_datetime_with_offset = end_datetime + self.SCHEDULE_OFFSET
        duration = end_datetime_with_offset - start_datetime_with_offset
        duration_in_minutes = duration.total_seconds() / 60
        channel = event['location']
        meta_data = json.loads(event['description'])
        scheduler = BackgroundScheduler()
        job = scheduler.add_job(self.kick_job, 'date', run_date=start_datetime_with_offset,
                                args=[RadikoRecorder(channel, duration_in_minutes,
                                                     meta_data['artist'], meta_data['album'],
                                                     True),
                                      scheduler])
        logging.info('Register radiko schedule on {} at {}'.format(
            channel, start_datetime_with_offset))
        self._schedules[event_key] = (scheduler, job)
        scheduler.start()

    def kick_job(self, radiko_recorder, scheduler):
        'Run RadikoRecorder job.'
        radiko_recorder.run()


if __name__ == '__main__':
    init_logging()
    task = GCalRadikoTask(None)
    while True:
        sleep(1)
