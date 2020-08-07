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

from apscheduler.schedulers.blocking import BlockingScheduler
import time
from datetime import datetime

class Schedule:

    def __init__(self):

        self.scheduler = BlockingScheduler()

    def string_to_datetime(self, input_string):

        output_date = datetime.strptime(input_string, '%Y-%m-%dT%H:%M:%S%z')
        return output_date

if __name__ == '__main__':

    scheduler = BlockingScheduler()
    hue = HueControl()
    hue.get_lights_data()
    light_selected = hue.select_light('Study light')

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