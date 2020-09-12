""" Module to schedule hue bulb jobs based on Google Calendar events

    - Get list of gcalendar meetings
    - Check those that are 
    - Convert

"""

if __name__ == '__main__' and __package__ is None:
    import sys
    from os import path
    sys.path.append( path.dirname( path.dirname (path.dirname( path.abspath(__file__) ) ) ))
    from connector.pipelines.hue import HueControl

from apscheduler.schedulers.background import BackgroundScheduler
import time
from datetime import datetime

class Schedule:

    def __init__(self, cal_events):

        self.sched = BackgroundScheduler(daemon=True)
        self.gcalendar_events = cal_events

    def current_jobs(self):

        print(self.gcalendar_events)
        print(self.sched.get_jobs())

    def add_start_events(self, start_function):

        for i in self.gcalendar_events:

            self.sched.add_job(start_function, 'date', run_date=i['start_time'])

    def add_end_events(self, end_function):

        print('end function here')

    def start_scheduler(self):

        self.sched.start()
            

if __name__ == '__main__':

    gcalendar_events = [
        {'start_time': '2020-09-13T15:45:00+01:00', 
        'end_time': '2020-09-13T16:30:00+01:00', 
        'event_name': 'Weekly Connect', 
        'status': 'confirmed'}, 
        {'start_time': '2020-09-13T19:30:00+01:00', 
        'end_time': '2020-09-13T20:30:00+01:00', 
        'event_name': 'Torchlight', 
        'status': 'confirmed'}
    ]

    hue = HueControl()
    hue.get_lights()
    light_selected = hue.select_lights('Study light', 'light')

    sched = Schedule(gcalendar_events)
    sched.add_start_events(hue.switch_lights)
    sched.start_scheduler()
    sched.current_jobs()

    """
    def job_1():

        print('hello this is job 1')

    def job_2():

        print('hello this is job 2')

    def job_3(scheduler_object):

        print('shut down job')
        scheduler_object.pause()


    scheduler.add_job(job_1, 'interval', id='job_1', seconds=3)
    scheduler.add_job(job_2, 'interval', id='job_2', seconds=7)
    scheduler.add_job(job_3, 'interval', args=[scheduler], id='job_3', seconds=10)

    print(scheduler.get_jobs())

    scheduler.start()

    print('got here')

    #scheduler.add_job(hue.switch_light, 'interval', id='test1', seconds=10)

    #scheduler.start()
    """