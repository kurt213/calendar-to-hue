if __name__ == '__main__' and __package__ is None:
    import sys
    from os import path
    sys.path.append( path.dirname( path.dirname (path.dirname( path.abspath(__file__) ) ) ))

from re import X
import requests
import json
import time
from os.path import exists
import random

class HueAccess:

    def __init__(self):

        self._check_hue_ip()
        # authorise api - check whether you get `link button not pressed` or success
        # (https://developers.meethue.com/develop/hue-api-v2/getting-started/)
        # if success - store the key in secrets.py

    def _get_hue_ip(self):

        bridge_ip_request = requests.get('https://discovery.meethue.com/')
            
        if bridge_ip_request.status_code == 200:

            bridge_ip_json = json.loads(bridge_ip_request.content)
            bridge_ip = bridge_ip_json[0]['internalipaddress']

            return bridge_ip, bridge_ip_json        
        
        else:
            print('could not access API - exiting')
            exit()


    def _get_hue_json_ip(self):

        if exists('connector/access/hue_ip.json'):

                with open('connector/access/hue_ip.json', 'r') as f:
                    json_output = json.load(f)
                f.close()

                return json_output[0]['internalipaddress']
        else:
            # print('ip file does not exist - should run Hue Discovery API')
            exit()

    def _save_hue_ip_json(self, bridge_json):

        with open('connector/access/hue_ip.json', 'w') as f:
            json.dump(bridge_json, f)
        f.close()

    def _check_hue_ip(self):

        if exists('connector/access/hue_ip.json'):
            # print('ip file exists - use this')
            bridge_ip = self._get_hue_json_ip()

        else:
            # print('ip file does not exist - run Hue Discovery API')
            bridge_ip, bridge_ip_json = self._get_hue_ip()
            self._save_hue_ip_json(bridge_ip_json)
        
        # print(bridge_ip)
        self.bridge_ip = bridge_ip
        
    def test_hue_ip(self):

        json_ip = self._get_hue_json_ip()
        hue_ip, json_response = self._get_hue_ip()

        if not json_ip:
            print("stored JSON ip does not exist")
        elif not hue_ip:
            print("could not retrieve Hue ip from API")
        else:
            if hue_ip == json_ip:
                print(f"stored ip: {json_ip} and hue ip: {hue_ip} successfully match")
            else:
                print(f"ERROR: stored ip: {json_ip} and hue ip: {hue_ip} do not match")
                print("setting JSON to latest ip address")
                self._save_hue_ip_json(json_response)


class HueControl:

    def __init__(self, hue_ip=False):
        
        if not hue_ip:
            print('Hue IP not provided - exiting')
            exit()
        else:
            self.hue_ip = hue_ip

        if exists('connector/access/hue_secrets.json'):
            with open('connector/access/hue_secrets.json', 'r') as f:
                json_output = json.load(f)
                self.hue_app_key = json_output['hue_app_key']
                self.request_header = {"hue-application-key": self.hue_app_key}
            f.close()

        try:

            devices_request = "https://{}/clip/v2/resource/device".format(self.hue_ip)
            self.get_devices_response = requests.get(devices_request, headers=self.request_header, verify=False, timeout=1.000)

            rooms_request = "https://{}/clip/v2/resource/room".format(self.hue_ip)
            self.get_rooms_response = requests.get(rooms_request, headers=self.request_header, verify=False, timeout=1.000)

        except requests.exceptions.Timeout as e:

            # print(e)
            self.get_devices_response = None
            self.get_rooms_response = None

    def show_raw_data(self, device_or_room):

        if device_or_room == 'device':
            raw_devices_json = self.get_devices_response.content
            parsed_devices_json = json.loads(raw_devices_json)
            print(json.dumps(parsed_devices_json, indent=2, sort_keys=True))

            # Temp store json data
            with open('devices_data.json', 'w') as f:
                json.dump(parsed_devices_json, f)
            f.close()            

        elif device_or_room == 'room':
            raw_rooms_json = self.get_rooms_response.content
            parsed_rooms_json = json.loads(raw_rooms_json)
            print(json.dumps(parsed_rooms_json, indent=2, sort_keys=True))

        else:
            print("'devices or 'room' not selected")

    def get_device_lists(self):

        devices_json = json.loads(self.get_devices_response.content)
        devices_json_list = devices_json['data']
        rooms_json = json.loads(self.get_rooms_response.content)
        rooms_json_list = rooms_json['data']

        self.lights_list = self._get_device_data(devices_json_list, 'light')
        self.rooms_list = self._get_device_data(rooms_json_list, 'grouped_light')

        self.devices_list = self.lights_list + self.rooms_list

        return self.devices_list

    def _get_device_data(self, json_content, type='unknown'):

        output_list = []

        for item in json_content:
            if 'id_v1' in item:
                if 'lights' in item['id_v1'] or 'room' in item['type']:
                    item_name = item['metadata']['name']
                    rid_list = item['services']
                    
                    for r in rid_list:
                        if 'light' in r['rtype']:
                            d_id = r['rid']    

                    items_dict = {
                        'rid': d_id,
                        'name': item_name,
                        'type': type
                    }
                    output_list.append(items_dict)
        
        return output_list

    def get_device_status(self, device_name):

        selected_device = False

        for d in self.devices_list:
            if d['name'] == device_name:
                selected_device = d
        
        if not selected_device:
            print('Cant find device - exiting')
            exit()

        status_request = "https://{}/clip/v2/resource/{}/{}".format(self.hue_ip, selected_device['type'], selected_device['rid'])
        get_status_response = requests.get(status_request, headers=self.request_header, verify=False)
        self.status_json = json.loads(get_status_response.content)
        json_data = self.status_json['data'][0]

        selected_device_status = {
            "on": json_data['on']['on'],
            "brightness": json_data['dimming']['brightness']
        }

        if selected_device['type'] == 'light':
            color_status = {
                "color_x": json_data['color']['xy']['x'],
                "color_y": json_data['color']['xy']['y']
            }
            selected_device_status = {**selected_device_status, **color_status}

        selected_device_data = {**selected_device, **selected_device_status}
        return selected_device_data


    def switch_lights(self, device_name, on_off_target_status=False, current_device_status=False):

        if not current_device_status:
            current_device_status = self.get_device_status(device_name)

        if not on_off_target_status:
            if current_device_status['on'] == True:
                switch_instruction = 'false'
            elif current_device_status['on'] == False:
                switch_instruction = 'true'
            else:
                print("switch status error - exiting")
                exit()
        elif on_off_target_status == 'on':
            switch_instruction = 'true'
        elif on_off_target_status == 'off':
                switch_instruction = 'false'
        else:
            print('invalid target switch status - exiting')
            exit()
        
        request_body = '{"on":{"on":' + switch_instruction + '}}'
        
        switch_request = "https://{}/clip/v2/resource/{}/{}".format(self.hue_ip, current_device_status['type'], current_device_status['rid'])
        switch_response = requests.put(switch_request, headers=self.request_header, data=request_body, verify=False)

        if switch_response.status_code == 200:
            print("light switched successfully")
        else:
            print("error - issue switching light")
            print(switch_response.content)
        
    def switch_colour_brightness(self, device_name, x=False, y=False, brightness=False, current_device_status=False):

        if not current_device_status:
            current_device_status = self.get_device_status(device_name)

        if current_device_status['on'] == False:
            print('light is off, switch on before changing colour - exiting')
            exit()

        if not x and not y and not brightness:
            print('no statuses set - exiting')
            return None

        xy_body = False
        brightness_body = False

        if not x or not y:
            print('no x or y values - skipping')
        else:
            xy_body = '"color":{"xy":{"x":' + str(x) + ',"y":' + str(y) + '}}'

        if not brightness:
            print('no x or y values - skipping')
        else:
            brightness_body = '"dimming":{"brightness":' + str(brightness) + '}'

        if xy_body and brightness_body:
            print('changing color & brightness')
            request_body = '{' + xy_body + ',' + brightness_body + '}'
        elif xy_body:
            print('changing color')
            request_body = '{' + xy_body + '}'
        elif brightness:
            print('changing brightness')
            request_body = '{' + brightness_body + '}'

        print(request_body)

        color_request = "https://{}/clip/v2/resource/{}/{}".format(self.hue_ip, current_device_status['type'], current_device_status['rid'])
        color_response = requests.put(color_request, headers=self.request_header, data=request_body, verify=False)

        if color_response.status_code == 200:
            print("light changed successfully")
        else:
            print("error - issue changing light")
            print(color_response.content)

    def flash_lights(self, device_name, number_flashes, x=False, y=False, brightness=False):

        current_device_status = self.get_device_status(device_name)

        self.switch_lights(device_name, on_off_target_status='on', current_device_status=current_device_status)
        time.sleep(2)
        self.switch_colour_brightness(device_name,x, y, brightness)

        for x in range(number_flashes):
            self.switch_lights(device_name, on_off_target_status='off', current_device_status=current_device_status)
            time.sleep(1)
            self.switch_lights(device_name, on_off_target_status='on', current_device_status=current_device_status)
            time.sleep(2)

if __name__ == '__main__':

    hue_access = HueAccess()

    print(hue_access.bridge_ip)
    hue = HueControl(hue_access.bridge_ip)
    devices_list = hue.get_device_lists()
    hue.get_device_status('Study Lamp')
    hue.get_device_status('Upstairs Office')
    hue.switch_lights('Study Lamp')

    #x = random.uniform(0.0001, 1.0000)
    #y = random.uniform(0.0001, 1.0000)
    #brightness = random.uniform(100, 100)
    #hue.switch_colour_brightness('Landing', x, y, brightness)
    #hue.flash_lights('Study Lamp', 5)