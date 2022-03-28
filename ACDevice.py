
import json
import paho.mqtt.client as mqtt

import Constant

HOST = "localhost"
PORT = 1883
    
class AC_Device():
    
    _MIN_TEMP = 18  
    _MAX_TEMP = 32  

    def __init__(self, device_id, room):
        
        self._device_id = device_id
        self._room_type = room
        self._temperature = 22
        self._device_type = Constant.AC
        self._device_registration_flag = False
        self.client = mqtt.Client(self._device_id)  
        self.client.on_connect = self._on_connect  
        self.client.on_message = self._on_message  
        self.client.on_disconnect = self._on_disconnect
        self.client.connect(HOST, PORT, keepalive=60)  
        self.client.loop_start()  
        self._register_device(self._device_id, self._room_type, self._device_type)
        self._switch_status = "OFF"

    # calling registration method to register the device
    def _register_device(self, device_id, room_type, device_type):
        self._device_registration_flag = True
        self.client.publish(Constant.CONNECT, payload=json.dumps(
            {"device_id": device_id,
             "device_type": device_type,
             "device_room": room_type,
             "registration_status": self._device_registration_flag
             }))

    # Connect method to subscribe to various topics. 
    def _on_connect(self, client, userdata, flags, result_code):
        if result_code == 0:
            self.client.subscribe(Constant.REGISTRATION_SUCCESS + self._device_id)
            self.client.subscribe(Constant.HEALTH_CHECK + self._device_id)
            self.client.subscribe(Constant.SWITCH_ON_OFF + "#")
            self.client.subscribe(Constant.CHANGE_STATE + "#")
        else:
            print("Error while connecting to MQTT server.")

    # Connect method to subscribe to various topics.
    def _on_disconnect(self, client, userdata, flags, result_code):
        self.client.publish("my_smart_home/disconnect", "AC-BLUE-STAR,AC,Bedroom")


    # method to process the recieved messages and publish them on relevant topics 
    # this method can also be used to take the action based on received commands
    def _on_message(self, client, userdata, msg):
        if msg.topic.__contains__(Constant.REGISTRATION_SUCCESS):
            print("Registration status- ", str(msg.payload.decode("utf-8")))
        if msg.topic.__contains__(Constant.HEALTH_CHECK):
            self.client.publish(Constant.STATUS + self._device_id, json.dumps(
                                {
                                    'device_id': self._device_id,
                                    'switch_state': self._get_switch_status(),
                                    'temperature': self._get_temperature()
                                }))
        if msg.topic.__contains__(Constant.SWITCH_ON_OFF + self._device_id) \
                or msg.topic.__contains__(Constant.SWITCH_ON_OFF + Constant.AC) \
                or msg.topic.__contains__(Constant.SWITCH_ON_OFF + self._room_type):
            output = self._set_switch_status(msg.payload.decode('utf-8'))
            if output == Constant.SUCCESS:
                self.client.publish(Constant.SWITCH_ON_OFF + "output", json.dumps(
                    {'status': Constant.SUCCESS,
                     'message': f"{self._device_id} in room {self._room_type} is successfully"
                                f" switched {msg.payload.decode('utf-8')}"
                     }))
            if output == Constant.SAME_VALUE:
                self.client.publish(Constant.SWITCH_ON_OFF + "output", json.dumps(
                    {'status': Constant.INFO,
                     'message': f"{self._device_id} in room {self._room_type} is already"
                                f" switched {msg.payload.decode('utf-8')}"
                     }))

        if msg.topic.__contains__(Constant.CHANGE_STATE + self._device_id) \
            or msg.topic.__contains__(Constant.CHANGE_STATE + Constant.AC + "/" + self._room_type):
            output = self._set_temperature(msg.payload.decode('utf-8'))
            if output == Constant.SUCCESS:
                self.client.publish(Constant.CHANGE_STATE + "output", json.dumps(
                                    {'status': Constant.SUCCESS,
                                     'message': f"Temperature of {self._device_id} in room {self._room_type} "
                                                f"is changed successfully to {msg.payload.decode('utf-8')} degree Celsius"
                                     }))
            if output == Constant.SAME_VALUE:
                self.client.publish(Constant.CHANGE_STATE + "output", json.dumps(
                                    {'status': Constant.INFO,
                                     'message': f"Couldn't able to change Temperature of {self._device_id} "
                                                f"in room {self._room_type} to {msg.payload.decode('utf-8')},"
                                                f" it might be off or already having same temperature"
                                     }))
            if output == Constant.INVALID_VALUE:
                self.client.publish(Constant.CHANGE_STATE + "output", json.dumps(
                                    {'status': Constant.INFO,
                                     'message': f"Temperature change failed of {self._device_id} "
                                                f"in room {self._room_type} to {msg.payload.decode('utf-8')},"
                                                f" invalid value provided"
                                     }))

    # Getting the current switch status of devices
    def _get_switch_status(self):
        return self._switch_status

    # Setting the the switch of devices
    def _set_switch_status(self, switch_status):
        if self._switch_status != switch_status:
            self._switch_status = switch_status
            return Constant.SUCCESS
        else:
            return Constant.SAME_VALUE

    # Getting the temperature for the devices
    def _get_temperature(self):
        return self._temperature

    # Setting up the temperature of the devices
    def _set_temperature(self, temperature):
        if self._get_switch_status() == "ON" and self._temperature != temperature:
            if 22 < int(temperature) < 30:
                self._temperature = temperature
                return Constant.SUCCESS
            else:
                return Constant.INVALID_VALUE
        else:
            return Constant.SAME_VALUE


    
