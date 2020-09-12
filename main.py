""" Program starting module



"""

from connector.pipelines import gcalendar, hue, schedule_jobs

def main():

    # Get GCalendar data
    events = gcalendar.get_today_events()
    print(events)

    # Connect to Hue lighting system
    hue_control = hue.HueControl()
    #groups_data = hue_control.get_groups_data()
    #group_selected = hue_control.select_group('All Lights')
    hue_control.get_lights_data()
    light_selected = hue_control.select_light('Study light')

    if light_selected:
        hue_control.switch_light('on', True)

if __name__ == '__main__':

    main()
