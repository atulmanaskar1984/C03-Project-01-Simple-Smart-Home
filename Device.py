class Device():
    def __init__(self, device_id, device_type, device_installation_room):
        self.device_id = device_id
        self.device_type = device_type
        self.device_installation_room = device_installation_room

    def print_me(self):
        print(f'Device {self.device_type} with Id {self.device_id} is installed in {self.device_installation_room}')
