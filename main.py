""" Program starting module



"""

from connector.pipelines import gcalendar, hue, schedule_jobs
from connector.access import flask_secret_key
from flask_app.app import app
import os

def main():

    #app.run('127.0.0.1', port=5001, debug=True)
    app.run('0.0.0.0', port=5001, debug=True)

if __name__ == '__main__':

    #flask_secret_key()
    main()
