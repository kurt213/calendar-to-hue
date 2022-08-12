if __name__ == '__main__' and __package__ is None:
    import sys
    from os import path
    sys.path.append( path.dirname( path.dirname (path.dirname( path.abspath(__file__) ) ) ))

import socket
import requests
import json
import time
import pprint
from os.path import exists

from connector.access import secrets

class HueAccess:

    def __init__(self):

        self._get_hue_ip()
        # authorise api - check whether you get `link button not pressed` or success
        # (https://developers.meethue.com/develop/hue-api-v2/getting-started/)
        # if success - store the key in secrets.py

    def _get_hue_ip(self):

        if exists('connector/access/hue_ip.json'):
                print('ip file exists - use this')

                with open('connector/access/hue_ip.json', 'r') as f:
                    json_output = json.load(f)
                f.close()

                bridge_ip = json_output[0]['internalipaddress']
        else:
            print('ip file does not exist - run Hue Discovery API')

            bridge_ip_request = requests.get('https://discovery.meethue.com/')

            if bridge_ip_request.status_code == 200:

                bridge_ip_json = json.loads(bridge_ip_request.content)
                bridge_ip = bridge_ip_json[0]['internalipaddress']

                with open('connector/access/hue_ip.json', 'w') as f:
                    json.dump(bridge_ip_json, f)
                f.close()
            
            else:

                print('could not access API - exiting')
                exit()
        
        print(bridge_ip)
        self.bridge_ip = bridge_ip

class HueControl:

    def __init__(self, hue_ip=False):
        
        if not hue_ip:
            print('Hue IP not provided - exiting')
            exit()
        else:
            self.hue_ip = hue_ip

        self.hue_user = secrets.username

        lights_request = "https://{}/clip/v2/resource/device".format(self.hue_ip)
        lights_request_header = {"hue-application-key": self.hue_user}
        self.get_lights_response = requests.get(lights_request, headers=lights_request_header, verify=False)

        #groups_request = "https://{}/api/{}/groups".format(self.hue_ip, self.hue_user)
        #self.get_groups_response = requests.get(groups_request)

        self.get_lights()
        #self.show_raw_data('light')

    def show_raw_data(self, light_or_group):

        if light_or_group == 'light':

            raw_lights_json = self.get_lights_response.content
            parsed_lights_json = json.loads(raw_lights_json)
            print(json.dumps(parsed_lights_json, indent=2, sort_keys=True))

            # Temp store json data
            with open('lights_data.json', 'w') as f:
                json.dump(parsed_lights_json, f)
            f.close()            

        elif light_or_group == 'group':

            raw_groups_json = self.get_groups_response.content
            parsed_groups_json = json.loads(raw_groups_json)
            print(json.dumps(parsed_groups_json, indent=2, sort_keys=True))

        else:

            print("'light' or 'group' not selected")

    def get_lights(self):

        lights_json = json.loads(self.get_lights_response.content)
        groups_json = json.loads(self.get_groups_response.content)
        self.lights_list = []
        self.groups_list = []

        for l_id, l in lights_json.items():
            lights_dict = {
                'id': l_id,
                'name': l['name']
            }
            state_dict = l['state']
            combined_dict = dict(**lights_dict, **state_dict)
            self.lights_list.append(combined_dict)

        for g_id, g in groups_json.items():
            groups_dict = {
                'id': g_id,
                'name': g['name']
            }
            state_dict = g['state']
            combined_dict = dict(**groups_dict, **state_dict)
            self.groups_list.append(combined_dict)

        return self.lights_list, self.groups_list

    def select_lights(self, light_group_name, light_or_group):

        self.current_lights = False

        if light_or_group == 'light':

            for sl in self.lights_list:
                if sl['name'] == light_group_name:
                    self.current_lights = sl
                    break
            if self.current_lights:
                print('light selected')
                self.light_or_group_url = 'lights'
                # Used in request to check/switch single light on
                self.switch_body_req = 'on'
                self.state_action_req = 'state'
                return self.current_lights
            else:
                print('light with provided name does not exist')

        elif light_or_group == 'group':

            for sg in self.groups_list:
                if sg['name'] == light_group_name:
                    self.current_lights= sg
                    break
            if self.current_lights:
                print('group selected')
                self.light_or_group_url = 'groups'
                # Used in request to check/switch single light on
                self.switch_body_req = 'all_on'
                self.state_action_req = 'action'
                return self.current_lights
            else:
                print('group with provided name does not exist')                

        else:
            print("error: select 'light' or 'group'")    

    def store_lights_state(self):

        print('lights store state goes here - for when a user')

    def switch_lights(self):

        if self.current_lights:

            if self.current_lights[self.switch_body_req]:
                sl_command='false'
            else:
                sl_command='true'

            lights_id = self.current_lights['id']

            sl_url = "http://{}/api/{}/{}/{}/{}".format(self.hue_ip, self.hue_user, self.light_or_group_url, lights_id, self.state_action_req)
            sl_body = '{"on":' + sl_command + '}'
            
            sl_response = requests.put(sl_url,
            data=sl_body
            )

            if sl_response.ok:
                print('lights switched successfully')
            else:
                print('lights switch failure')

        else:
            print('lights with provided name does not exist')
        
    def switch_colour(self, x, y):

        if self.current_lights:

            lights_id = self.current_lights['id']
            lc_url = "http://{}/api/{}/{}/{}/{}".format(self.hue_ip, self.hue_user, self.light_or_group_url, lights_id, self.state_action_req)
            lc_body = '{"xy":[' + str(x) + ',' + str(y) + ']}'
            
            lc_response = requests.put(lc_url,
            data=lc_body
            )
        else:
            print('light with provided name does not exist')

    def flash_lights(self, number_flashes):

        if self.current_lights:

            if self.current_lights[self.switch_body_req]:
                sl_command='false'
            else:
                sl_command='true'

            number_iterations = number_flashes * 2

            for i in range(number_iterations):

                lights_id = self.current_lights['id']
                sl_url = "http://{}/api/{}/{}/{}/{}".format(self.hue_ip, self.hue_user, self.light_or_group_url, lights_id, self.state_action_req)
                sl_body = '{"on":' + sl_command + '}'

                sl_response = requests.put(sl_url,
                data=sl_body
                )

                if sl_command == 'true':
                    sl_command = 'false'
                else:
                    sl_command = 'true'

                time.sleep(2)

    def meeting_start(self, light_group, switch_action, x, y, number_flashes=3):

        print('meeting start combo functionality goes here')

if __name__ == '__main__':

    """
    hue = HueControl()
    hue.get_lights()
    lights_selected = hue.select_lights('Study light','light')
    #lights_selected = hue.select_lights('All Lights', 'group')

    if lights_selected:
        hue.switch_lights()
        # red
        #hue.switch_colour(0.675, 0.322)
        # blue
        #hue.switch_colour(0.25, 0.25)        
        #hue.flash_lights(3)
    else:
        print('no light selected')
    """

    #hue_access = HueAccess()
    #hue = HueControl(hue_access.bridge_ip)

    with open('lights_data.json', 'r') as f:
        json_output = json.load(f)
    f.close()

    target_bulb_name = 'Study Desk'
    
    device_list = json_output['data']
    for d in device_list:
        if d['metadata']['name'] == target_bulb_name:
            found_device = d
            found_rid_list = d['services']
    
    for r in found_rid_list:
        if r['rtype'] == 'light':
            found_rid_light_control = r['rid']
            