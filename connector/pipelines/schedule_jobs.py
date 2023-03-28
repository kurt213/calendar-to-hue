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

        jobs_list = []
        for j in self.sched.get_jobs():
            jobs_list.append({
                'job_id': j.id,
                'job_name': j.name,
                'trigger_time': j.trigger.run_date.strftime("%Y-%m-%d, %H:%M:%S"),
                'trigger_function': j.func.__name__
            })
        
        return jobs_list

    def _rename_event(self, event_name):
        output_event_name = event_name.lower()
        output_event_name = output_event_name.replace(" ", "_")
        return output_event_name

    def add_start_events(self, start_function):

        for i in self.cal_events:

            event_name = self._rename_event(i['event_name'])
            self.sched.add_job(start_function, 'date', run_date=i['start_time'], name=event_name)

    def add_end_events(self, end_function):

        for i in self.cal_events:

            event_name = self._rename_event(i['event_name'])
            self.sched.add_job(end_function, 'date', run_date=i['end_time'], name=event_name)

    def start_scheduler(self):

        self.sched.start()
            

if __name__ == '__main__':

    def test_event():

        print('hello - this is your scheduled event')

    gcalendar_events_examples = [
        {'start_time': '2023-01-09T23:22:00+01:00', 
        'end_time': '2023-01-09T23:24:00+01:00', 
        'event_name': 'Weekly Connect', 
        'status': 'confirmed'}, 
        {'start_time': '2023-01-09T23:28:00+01:00', 
        'end_time': '2023-01-09T23:29:00+01:00', 
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
    output_schedule = sched.current_jobs()
    print(output_schedule[0])
    print(output_schedule[1])