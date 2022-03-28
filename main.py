import time
from EdgeServer import Edge_Server
from LightDevice import Light_Device
from ACDevice import AC_Device

WAIT_TIME = 0.50

print("\nSmart Home Simulation started.")
# Creating the edge-server for the communication with the user

print("\n******************* REGSITRATION OF THE DEVICES THROUGH SERVER *******************")

my_smart_home_edge_server = Edge_Server('my_smart_home_edge_server')
time.sleep(WAIT_TIME)  

# Creating the light_device
print("Intitate the device creation and registration process." )
print("\nCreating the Light devices for their respective rooms.")
light_device_1 = Light_Device("light_1", "Kitchen")
time.sleep(WAIT_TIME)  

# Creating the ac_device  
print("\nCreating the AC devices for their respective rooms. ")
ac_device_1 = AC_Device("ac_1", "BR1")
time.sleep(WAIT_TIME)

ac_device_1 = AC_Device("AC_BLUE_STAR", "BR2")
time.sleep(WAIT_TIME)


ac_device_1 = AC_Device("AC_BLUE_STAR_1", "BR2")
time.sleep(WAIT_TIME)

# Printing list of registered devices
my_smart_home_edge_server.get_registered_device_list()
time.sleep(WAIT_TIME)

#Printing status of devices
print("******************* GETTING THE STATUS AND CONTROLLING THE DEVICES *******************")
print("******************* GETTING THE STATUS BY DEVICE_ID *******************")
my_smart_home_edge_server.get_status()
time.sleep(WAIT_TIME)

my_smart_home_edge_server.get_status("ac_1", "", "")
time.sleep(WAIT_TIME)

my_smart_home_edge_server.set("ON", "", "")
time.sleep(WAIT_TIME)

my_smart_home_edge_server.get_status()
time.sleep(WAIT_TIME)

print("******************* SETTING UP THE STATUS AND CONTROLLING BY THE DEVICE_TYPE *******************")
my_smart_home_edge_server.set_state_change(24, "AC", "ac_1")
time.sleep(WAIT_TIME)

my_smart_home_edge_server.get_status()
time.sleep(WAIT_TIME)

print("\nSmart Home Simulation stopped.")
my_smart_home_edge_server.terminate()
