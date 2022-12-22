from flask import Flask
from apscheduler.schedulers.background import BackgroundScheduler
from connector.pipelines import gcalendar, hue, schedule_jobs
import datetime

def sensor():
    current_time = datetime.datetime.now()
    print(f'Time now: {current_time}')
    jobs_list = sched.get_jobs()
    print(jobs_list)
    print(jobs_list[0])

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

def test_event(string_arg):
    print('this is your test event')
    print(string_arg)

sched = BackgroundScheduler(daemon=True)
sched.add_job(sensor,'cron',minute='*')
sched.add_job(test_event, 'date', ['test_string'], run_date='2022-12-21T16:44:00+00:00')

sched.start()

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


if __name__ == "__main__":
    app.run('127.0.0.1', port=5001, debug=True)
    print('hello')
