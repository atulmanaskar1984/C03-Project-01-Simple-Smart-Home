
import json
import time
import paho.mqtt.client as mqtt
from colorama import init, Fore
import Constant
from Device import Device

HOST = "localhost"
PORT = 1883     
WAIT_TIME = 0.25  

class Edge_Server:
    
    def __init__(self, instance_name):
        init(autoreset=True) #Initializing coloroma library
        self._instance_id = instance_name
        self.client = mqtt.Client(self._instance_id)
        self.client.on_connect = self._on_connect
        self.client.on_message = self._on_message
        self.client.connect(HOST, PORT, keepalive=60)
        self.client.loop_start()
        self._registered_list = []

    # Terminating the MQTT broker and stopping the execution
    def terminate(self):
        self.client.disconnect()
        self.client.loop_stop()

    # Connect method to subscribe to various topics.     
    def _on_connect(self, client, userdata, flags, result_code):
        if result_code == 0:
            print("Edge server connected to MQTT server successfully.")
            self.client.subscribe(Constant.MAIN_TOPIC)
            #self.client.subscribe(Constant.STATUS)
            #self.client.subscribe(Constant.SWITCH_ON_OFF + "output")
            #self.client.subscribe(Constant.CHANGE_STATE + "output")
        else:
            print("Error while connecting to MQTT server.")
        
    # method to process the recieved messages and publish them on relevant topics 
    # this method can also be used to take the action based on received commands
    def _on_message(self, client, userdata, msg):
        #print("message received ", str(msg.payload))
        #print("message topic ", msg.topic)

        if Constant.CONNECT == msg.topic:
            self.set_registered_device_list(str(msg.payload.decode("utf-8")))
        if msg.topic.__contains__(Constant.STATUS):
            device_details = json.loads(msg.payload.decode('utf-8'))
            print(f"Here is the current device-status for {device_details['device_id']} : {device_details}")
        if msg.topic.__contains__(Constant.SWITCH_ON_OFF + "output") \
                or msg.topic.__contains__(Constant.CHANGE_STATE + "output"):
            output = json.loads(msg.payload.decode('utf-8'))
            if output['status'] == Constant.SUCCESS:
                print(Fore.GREEN + output['message'])
            if output['status'] == Constant.INFO:
                print(Fore.YELLOW + output['message'])
            if output['status'] == Constant.FAILURE:
                print(Fore.RED + output['message'])

    # Returning the current registered list
    def get_registered_device_list(self):
        if len(self._registered_list) > 0:
            for device in self._registered_list:
                device.print_me()
        return self._registered_list

    # Set the current registered list
    def set_registered_device_list(self, str_device_details):
        device_details = json.loads(str_device_details)
        new_device = Device(device_details['device_id'], device_details['device_type'], device_details['device_room'])
        self._registered_list.append(new_device)
        print(f"\nRegistration request is acknowledged for device "
              f"'{device_details['device_id']}' in {device_details['device_room']}")
        print(f"Request is processed for {device_details['device_id']}.")
        self.client.publish(Constant.REGISTRATION_SUCCESS + device_details['device_id'],
                            f"{device_details['device_id']} Registered! - "
                            f"Registration status is available for '{device_details['device_id']}' "
                            f"- {device_details['registration_status']}")
        return

    # Getting the status for the connected devices
    def get_status(self, device_id="", device_type="", room_type=""):
        for device in self._registered_list:
            if len(device_id) > 0 or len(device_type) > 0 or len(room_type) > 0:
                if device_id == device.device_id \
                        or device_type == device.device_type \
                        or room_type == device.device_installation_room:
                    self.client.publish(Constant.HEALTH_CHECK + device.device_id)
            else:
                self.client.publish(Constant.HEALTH_CHECK + device.device_id)

    # Controlling and performing the operations on the devices
    # based on the request received
    def set(self, switch_on_off, device_id="", device_type="", room_type=""):
        if len(device_id) > 0:
            self.client.publish(Constant.SWITCH_ON_OFF + device_id, switch_on_off)
        if len(device_type) > 0:
            self.client.publish(Constant.SWITCH_ON_OFF + device_type, switch_on_off)
        if len(room_type) > 0:
            self.client.publish(Constant.SWITCH_ON_OFF + room_type, switch_on_off)
        if len(device_id) == 0 and len(device_type) == 0 and len(room_type) == 0:
            for device in self._registered_list:
                self.client.publish(Constant.SWITCH_ON_OFF + device.device_id, switch_on_off)

    def set_state_change(self, value, device_type, device_id="", room_type=""):
        if len(device_id) > 0:
            self.client.publish(Constant.CHANGE_STATE + device_id, value)
        if len(room_type) > 0:
            self.client.publish(Constant.CHANGE_STATE + device_type + '/' + room_type, value)
        if len(device_id) == 0 and len(room_type) == 0:
            for device in self._registered_list:
                if device.device_type == device_type:
                    self.client.publish(Constant.CHANGE_STATE + device.device_id, value)
