from flask import Flask, render_template, request, jsonify, session
import datetime

from connector.pipelines import gcalendar, hue, schedule_jobs
from connector.access import flask_secret_key

app = Flask(__name__)
app.secret_key = flask_secret_key.get_key()

@app.route('/')
def index():

    html_flag = True

    current_time = datetime.datetime.now()
    calendar_schedule = get_calendar_schedule(html_flag)
    hue_devices = get_hue_status(html_flag)
    trigger_events = get_event_schedule(html_flag, calendar_schedule)
    #session['event_schedule'] = get_event_schedule(html_flag, calendar_schedule)


    return render_template(
        'index.html', 
        current_time=current_time,
        calendar_schedule=calendar_schedule,
        event_schedule=trigger_events,
        hue_devices=hue_devices)

@app.route('/calendar', methods=['GET'])
def get_calendar_schedule(html_flag=False):
    try:
        google_calendar = gcalendar.CalendarAccess()
        events = google_calendar.get_today_events()
    except:
        events = ""

    if html_flag:
        return events
    else:
        return jsonify(events)

@app.route('/hue/devices', methods=['GET'])
def get_hue_status(html_flag=False):
    try:
        hue_access = hue.HueAccess()
        hue_control = hue.HueControl(hue_access.bridge_ip)

        if not hue_control.get_devices_response:
            return hue_control.get_devices_response
        else:
            if html_flag:
                return hue_control.get_device_lists()
            else:
                return jsonify(hue_control.get_device_lists()) 
    except:
        return ""

@app.route('/schedule', methods=['GET'])
def get_event_schedule(html_flag=False, gcalendar_events=False):
    def test_event():
        print('hello - this is your scheduled event')

    sched = schedule_jobs.Schedule(gcalendar_events)
    sched.add_start_events(test_event)
    sched.add_end_events(test_event)
    sched.start_scheduler()
    
    return sched.current_jobs()

if __name__ == "__main__":
    app.run('127.0.0.1', port=5001, debug=True)