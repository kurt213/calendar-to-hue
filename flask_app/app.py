from flask import Flask, render_template, request, jsonify
import datetime

from connector.pipelines import gcalendar, hue, schedule_jobs

app = Flask(__name__)

@app.route('/')
def index():

    html_flag = True

    current_time = datetime.datetime.now()
    calendar_schedule = get_calendar_schedule(html_flag)
    hue_devices = get_hue_status(html_flag)
    
    return render_template(
        'index.html', 
        current_time=current_time,
        schedule=calendar_schedule,
        hue_devices=hue_devices)

@app.route('/calendar', methods=['GET'])
def get_calendar_schedule(html_flag=False):
    google_calendar = gcalendar.CalendarAccess()
    events = google_calendar.get_today_events()
    if html_flag:
        return events
    else:
        return jsonify(events)

@app.route('/hue/devices', methods=['GET'])
def get_hue_status(html_flag=False):
    hue_access = hue.HueAccess()
    hue_devices = hue.HueControl(hue_access.bridge_ip)
    if html_flag:
        return hue_devices.get_device_lists()
    else:
        return jsonify(hue_devices.get_device_lists()) 

if __name__ == "__main__":
    app.run('127.0.0.1', port=5001, debug=True)