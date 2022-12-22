""" Module to schedule hue bulb jobs based on Google Calendar events

    - Get list of gcalendar meetings
    - Check those that are 
    - Convert

"""

if __name__ == '__main__' and __package__ is None:
    import sys
    from os import path
    sys.path.append( path.dirname( path.dirname (path.dirname( path.abspath(__file__) ) ) ))

from connector.pipelines.hue import HueAccess, HueControl
from apscheduler.schedulers.background import BackgroundScheduler
import time
from datetime import datetime
import random

class Schedule:

    def __init__(self, cal_events):

        self.sched = BackgroundScheduler(daemon=True)
        self.cal_events = cal_events

    def current_jobs(self):

        print(self.cal_events)
        print(self.sched.get_jobs())

    def add_start_events(self, start_function):

        for i in self.cal_events:

            self.sched.add_job(start_function, 'date', run_date=i['start_time'])

    def add_end_events(self, end_function):

        print('end function here')

    def start_scheduler(self):

        self.sched.start()
            

if __name__ == '__main__':

    def test_event():

        print('hello - this is your scheduled event')

    gcalendar_events_examples = [
        {'start_time': '2022-12-21T16:22:00+01:00', 
        'end_time': '2022-12-21T16:24:00+01:00', 
        'event_name': 'Weekly Connect', 
        'status': 'confirmed'}, 
        {'start_time': '2022-12-21T16:28:00+01:00', 
        'end_time': '2020-12-21T16:29:00+01:00', 
        'event_name': 'Torchlight', 
        'status': 'confirmed'}
    ]

    #hue_access = HueAccess()
    #hue = HueControl(hue_access.bridge_ip)
    #devices_list = hue.get_device_lists()

    x = random.uniform(0.0001, 1.0000)
    y = random.uniform(0.0001, 1.0000)
    brightness = random.uniform(50, 100)
    #hue.switch_colour_brightness('Upstairs Office', x, y, brightness)
    #hue.flash_lights('Upstairs Office', 5)

    #sched = Schedule(gcalendar_events_examples)
    #sched.add_start_events(hue.switch_lights)
    #sched.start_scheduler()
    #sched.current_jobs()

    sched = Schedule(gcalendar_events_examples)
    sched.add_start_events(test_event)
    sched.start_scheduler()
    sched.current_jobs()