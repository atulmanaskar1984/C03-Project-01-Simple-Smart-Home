import json
import paho.mqtt.client as mqtt
import Constant

HOST = "localhost"
PORT = 1883


class Light_Device():

    # setting up the intensity choices for Smart Light Bulb  
    _INTENSITY = ["LOW", "HIGH", "MEDIUM", "OFF"]

    def __init__(self, device_id, room):
        # Assigning device level information for each of the devices. 
        self._device_id = device_id
        self._room_type = room
        self._light_intensity = self._INTENSITY[0]
        self._device_type = Constant.LIGHT
        self._device_registration_flag = False
        self.client = mqtt.Client(self._device_id)  
        self.client.on_connect = self._on_connect  
        self.client.on_message = self._on_message  
        self.client.on_disconnect = self._on_disconnect  
        self.client.connect(HOST, PORT, keepalive=60)  
        self.client.loop_start()  
        self._register_device(self._device_id, self._room_type, self._device_type)
        self._switch_status = "OFF"

    def _register_device(self, device_id, room_type, device_type):
        self.client.publish(Constant.CONNECT, payload=json.dumps(
            {"device_id": device_id,
             "device_type": device_type,
             "device_room": room_type
             }))

    # Connect method to subscribe to various topics.
    def _on_connect(self, client, userdata, flags, result_code):
        if result_code == 0:
            print("Light Device connected to MQTT server successfully.")
            self.client.subscribe(Constant.REGISTRATION_SUCCESS + self._device_id)
            self.client.subscribe("my_smart_home/light/#")
            self.client.subscribe(Constant.HEALTH_CHECK + self._device_id)
            self.client.subscribe(Constant.SWITCH_ON_OFF + "#")
        else:
            print("Error while connecting to MQTT server.")

    # Connect method to subscribe to various topics.
    def _on_disconnect(self, client, userdata, flags, result_code):
        pass

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
                    'intensity': self._get_light_intensity()
                }))
        if msg.topic.__contains__(Constant.SWITCH_ON_OFF + self._device_id) \
                or msg.topic.__contains__(Constant.SWITCH_ON_OFF + Constant.LIGHT) \
                or msg.topic.__contains__(Constant.SWITCH_ON_OFF + self._room_type):
            if self._set_switch_status(msg.payload.decode('utf-8')):
                self.client.publish(Constant.SWITCH_ON_OFF + "output", json.dumps(
                    {'status': Constant.SUCCESS,
                     'message': f"{self._device_id} in room {self._room_type} is successfully"
                                f" switched {msg.payload.decode('utf-8')}"
                     }))
            else:
                self.client.publish(Constant.SWITCH_ON_OFF + "output", json.dumps(
                    {'status': Constant.INFO,
                     'message': f"{self._device_id} in room {self._room_type} is already"
                                f" switched {msg.payload.decode('utf-8')}"
                     }))

        if msg.topic.__contains__(Constant.CHANGE_STATE + self._device_id) \
                or msg.topic.__contains__(Constant.CHANGE_STATE + Constant.LIGHT) \
                or msg.topic.__contains__(Constant.CHANGE_STATE + self._room_type):
            output = self._set_light_intensity(msg.payload.decode('utf-8'))
            if output == Constant.SUCCESS:
                self.client.publish(Constant.CHANGE_STATE + "output", json.dumps(
                    {'status': Constant.SUCCESS,
                     'message': f"Intensity of {self._device_id} in room {self._room_type} "
                                f"is changed successfully to {msg.payload.decode('utf-8')}"
                     }))
            else:
                if output == Constant.SWITCHED_OFF:
                    message = f"Intensity of {self._device_id} in room {self._room_type} " \
                              f"can not be changed to {msg.payload.decode('utf-8')}, as it is currently SWITCHED OFF"
                if output == Constant.INVALID_VALUE:
                    message = f"Intensity of {self._device_id} in room {self._room_type}" \
                              f" can not be changed to {msg.payload.decode('utf-8')}, as it is not a valid value"
                if output == Constant.SAME_VALUE:
                    message = f"Intensity of {self._device_id} in room {self._room_type}" \
                              f" can not be changed to {msg.payload.decode('utf-8')}, as it is currently having same value"
                self.client.publish(Constant.CHANGE_STATE + "output", json.dumps(
                    {'status': Constant.FAILURE,
                     'message': message
                     }))

            self.client.publish(Constant.CHANGE_STATE + "output")

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

    # Getting the light intensity for the devices
    def _get_light_intensity(self):
        return self._light_intensity

    # Setting the light intensity for devices
    def _set_light_intensity(self, light_intensity):
        if self._get_switch_status() == "ON":
            if self._get_light_intensity() != light_intensity:
                if self._INTENSITY.__contains__(light_intensity):
                    self._light_intensity = light_intensity
                    return Constant.SUCCESS
                else:
                    return Constant.INVALID_VALUE
            else:
                return Constant.SAME_VALUE
        else:
            return Constant.SWITCHED_OFF
