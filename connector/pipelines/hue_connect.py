if __name__ == '__main__' and __package__ is None:
    import sys
    from os import path
    sys.path.append( path.dirname( path.dirname (path.dirname( path.abspath(__file__) ) ) ))

import socket
import requests
import json
import time

from connector.access import secrets

class Hue:

    def __init__(self, hue_ip=False):
        
        if not hue_ip:
            self.ip_address = socket.gethostbyname('Philips-hue-LC')
        else:
            self.ip_address = hue_ip

        self.hue_user = secrets.hue_user

        get_lights = "http://{}/api/{}/lights".format(self.ip_address, self.hue_user)
        self.get_lights_response = requests.get(get_lights)

    def lights_raw_data(self):

        raw_lights_json = self.get_lights_response.content
        parsed_lights_json = json.loads(raw_lights_json)
        print(json.dumps(parsed_lights_json, indent=2, sort_keys=True))

    def get_lights_data(self):

        lights_json = json.loads(self.get_lights_response.content)
        self.lights_list = []

        for l_id, l in lights_json.items():
            lights_dict = {
                'id': l_id,
                'name': l['name']
            }
            state_dict = l['state']
            combined_dict = dict(**lights_dict, **state_dict)
            self.lights_list.append(combined_dict)

        #print(self.lights_list)

    def select_light(self, light_name):

        self.current_light = False

        for sl in self.lights_list:
            if sl['name'] == light_name:
                self.current_light = sl
                break
        
        if self.current_light:
            print('light selected')
            return self.current_light
        else:
            print('light with provided name does not exist')


    def switch_light(self, target_state=False):

        if self.current_light:

            if self.current_light['on']:
                sl_command = 'false'
            else:
                sl_command = 'true'

            current_light_id = self.current_light['id']
            sl_url = "http://{}/api/{}/lights/{}/state".format(self.ip_address, self.hue_user, current_light_id)
            sl_body = '{"on":' + sl_command + '}'

            sl_response = requests.put(sl_url,
            data=sl_body
            )

            if sl_response.ok:
                print('light switched successfully')
            else:
                print('light switch failure')

        else:
            print('light with provided name does not exist')
        
    def switch_colour(self, x, y):

        if self.current_light:

            current_light_id = self.current_light['id']
            lc_url = "http://{}/api/{}/lights/{}/state".format(self.ip_address, self.hue_user, current_light_id)
            lc_body = '{"xy":[' + str(x) + ',' + str(y) + ']}'
            
            lc_response = requests.put(lc_url,
            data=lc_body
            )
        else:
            print('light with provided name does not exist')

    def flash_light(self, number_flashes):

        if self.current_light:

            if self.current_light['on']:
                sl_command = 'false'
            else:
                sl_command = 'true'

            number_iterations = number_flashes * 2

            for i in range(number_iterations):
                current_light_id = self.current_light['id']
                sl_url = "http://{}/api/{}/lights/{}/state".format(self.ip_address, self.hue_user, current_light_id)
                sl_body = '{"on":' + sl_command + '}'

                sl_response = requests.put(sl_url,
                data=sl_body
                )

                if sl_command == 'true':
                    sl_command = 'false'
                else:
                    sl_command = 'true'

                time.sleep(2)



if __name__ == '__main__':

    hue = Hue()
    hue.get_lights_data()
    light_selected = hue.select_light('Study light')

    if light_selected:
        hue.switch_light('on')
        hue.switch_colour(0.675, 0.322)
        hue.flash_light(3)
    else:
        print('no light selected')
