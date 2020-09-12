from flask import Flask
from apscheduler.schedulers.background import BackgroundScheduler
from connector.pipelines import gcalendar, hue, schedule_jobs

count = 0
def sensor():
    global count
    sched.print_jobs()
    print('Count: ' , count)
    count += 1

def change_light():

    print('change light executed')
    # Connect to Hue lighting system
    hue_control = hue.HueControl()
    #groups_data = hue_control.get_groups_data()
    #group_selected = hue_control.select_group('All Lights')
    hue_control.get_lights_data()
    light_selected = hue_control.select_light('Study light')

    if light_selected:
        hue_control.switch_light('on')

sched = BackgroundScheduler(daemon=True)
sched.add_job(sensor,'cron',minute='*')
sched.add_job(change_light, 'date', run_date='2020-08-13T11:55:00+01:00')

sched.start()

app = Flask(__name__)

if __name__ == "__main__":
    #app.run('0.0.0.0',port=5000)
    print('hello')
