import time

import Constant
from EdgeServer import Edge_Server
from LightDevice import Light_Device
from ACDevice import AC_Device

WAIT_TIME = 0.25

##IMP - Please do install "pip install colorama" before testing this code, it is used only to highlight print text for erros and warnings

print("\nSmart Home Simulation started.")
# Creating the edge-server for the communication with the user
my_smart_home_edge_server = Edge_Server('my_smart_home_edge_server')
time.sleep(WAIT_TIME)

print("\n******************* REGISTRATION OF THE DEVICES THROUGH SERVER *******************")
print("\n******************* REGISTRATION OF LIGHT DEVICES INITIATED *******************")

# Creating the light_device
print("\nInitiate the device creation and registration process.")
print("\nCreating the Light devices for their respective rooms.")
light_device_1 = Light_Device("light_1", "Kitchen")
time.sleep(WAIT_TIME)  

light_device_2 = Light_Device("light_2", "Garage")
time.sleep(WAIT_TIME)

light_device_3 = Light_Device("light_3", "BR1")
time.sleep(WAIT_TIME)

light_device_4 = Light_Device("light_4", "BR2")
time.sleep(WAIT_TIME)

light_device_5 = Light_Device("light_5", "Living")
time.sleep(WAIT_TIME)

print("\n******************* REGSITRATION OF AC DEVICES INITIATED *******************")
ac_device1 = AC_Device("ac_BLUE_STAR", "BR1")
time.sleep(WAIT_TIME)

ac_device2 = AC_Device("ac_DAIKIN_1", "Living")
time.sleep(WAIT_TIME)

ac_device3 = AC_Device("ac_DAIKIN_2", "Living")
time.sleep(WAIT_TIME)

print("\n******************* REGSITRED DEVICES ON THE SERVER *******************")
my_smart_home_edge_server.get_registered_device_list()

print("\n******************* GETTING THE STATUS AND CONTROLLING THE DEVICES *******************")
print("\n******************* GETTING THE STATUS BY DEVICE_ID *******************")
print("\nStatus based on device_id:")

print("\nCommand ID 1 - my_smart_home_edge_server.get_status('light_1')")
my_smart_home_edge_server.get_status('light_1')
time.sleep(WAIT_TIME)

print("\nCommand ID 2 - my_smart_home_edge_server.get_status('light_2')")
my_smart_home_edge_server.get_status('light_2')
time.sleep(WAIT_TIME)

print("\nCommand ID 3 - my_smart_home_edge_server.get_status('light_3')")
my_smart_home_edge_server.get_status('light_3')
time.sleep(WAIT_TIME)

print("\nCommand ID 4 - my_smart_home_edge_server.get_status('light_4')")
my_smart_home_edge_server.get_status('light_4')
time.sleep(WAIT_TIME)

print("\nCommand ID 5 - my_smart_home_edge_server.get_status('light_5')")
my_smart_home_edge_server.get_status('light_5')
time.sleep(WAIT_TIME)

print("\nCommand ID 6 - my_smart_home_edge_server.get_status('ac_BLUE_STAR')")
my_smart_home_edge_server.get_status('ac_BLUE_STAR')
time.sleep(WAIT_TIME)

print("\nCommand ID 7 - my_smart_home_edge_server.get_status('ac_DAIKIN_1')")
my_smart_home_edge_server.get_status('ac_DAIKIN_1')
time.sleep(WAIT_TIME)

print("\nCommand ID 8 - my_smart_home_edge_server.get_status('ac_DAIKIN_2')")
my_smart_home_edge_server.get_status('ac_DAIKIN_2')
time.sleep(WAIT_TIME)

print("\n******************* GETTING THE STATUS BY DEVICE_TYPE *******************")
print("\nStatus based on: LIGHT DEVICE TYPE")

print("\nCommand ID 9 - my_smart_home_edge_server.get_status('', Constant.LIGHT)")
my_smart_home_edge_server.get_status('', Constant.LIGHT)
time.sleep(WAIT_TIME)

print("\nStatus based on: AC DEVICE TYPE")
print("\nCommand ID 10 - my_smart_home_edge_server.get_status('', Constant.AC)")
my_smart_home_edge_server.get_status('', Constant.AC)
time.sleep(WAIT_TIME)

print("\n******************* GETTING THE STATUS BY ROOM_TYPE *******************")
print("\nStatus based on room:")
print("\nCommand ID 11 - Living Room - my_smart_home_edge_server.get_status('', '', 'Living')")
my_smart_home_edge_server.get_status('', '', 'Living')
time.sleep(WAIT_TIME)

print("\n******************* GETTING THE STATUS BY ENTIRE_HOME *******************")
print("\nStatus based on room:")
print("\nCommand ID 12 - Entire Home - my_smart_home_edge_server.get_status()")
my_smart_home_edge_server.get_status()
time.sleep(WAIT_TIME)

print("\n******************* SETTING UP THE STATUS AND CONTROLLING THE DEVICE_ID *******************")
print("\nControlling the devices based on ID:")
print("\nCommand ID 13 - my_smart_home_edge_server.set('ON', 'light_1')")
my_smart_home_edge_server.set("ON", "light_1")
time.sleep(WAIT_TIME)

print("\nCommand ID 14 - my_smart_home_edge_server.set('ON', 'ac_BLUE_STAR')")
my_smart_home_edge_server.set("ON", "ac_BLUE_STAR")
time.sleep(WAIT_TIME)

print("\nCommand ID 15 - my_smart_home_edge_server.set_state_change('MEDIUM', Constant.LIGHT, 'light_1')")
my_smart_home_edge_server.set_state_change("MEDIUM", Constant.LIGHT, "light_1")
time.sleep(WAIT_TIME)
my_smart_home_edge_server.get_status('light_1')
time.sleep(WAIT_TIME)


print("\nCommand ID 16 - my_smart_home_edge_server.set_state_change(29, Constant.AC, 'ac_BLUE_STAR)")
my_smart_home_edge_server.set_state_change(29, Constant.AC, "ac_BLUE_STAR")
time.sleep(WAIT_TIME)
my_smart_home_edge_server.get_status('AC_BLUE_STAR')
time.sleep(WAIT_TIME)

print("\nCommand ID 17 - my_smart_home_edge_server.set_state_change('HIGH', Constant.LIGHT, 'light_2')")
my_smart_home_edge_server.set("ON", "light_2") #need to switch on light before changing its intensity
time.sleep(WAIT_TIME)
my_smart_home_edge_server.set_state_change("HIGH", Constant.LIGHT, "light_2")
time.sleep(WAIT_TIME)
my_smart_home_edge_server.get_status('light_2')
time.sleep(WAIT_TIME)

print("\n******************* SETTING UP THE STATUS AND CONTROLLING BY THE DEVICE_TYPE *******************")
print("\nCommand ID 18 - my_smart_home_edge_server.set_state_change('MEDIUM'', Constant.LIGHT)")
my_smart_home_edge_server.set("ON", "", Constant.AC) #need to switch on light before changing its intensity
time.sleep(WAIT_TIME)
my_smart_home_edge_server.set_state_change(21, Constant.LIGHT)
time.sleep(WAIT_TIME)
my_smart_home_edge_server.get_status('', Constant.LIGHT)
time.sleep(WAIT_TIME)


print("\nCommand ID 19 - my_smart_home_edge_server.set_state_change('MEDIUM'', Constant.LIGHT)")
my_smart_home_edge_server.set("ON", "", Constant.LIGHT) #need to switch on light before changing its intensity
time.sleep(WAIT_TIME)
my_smart_home_edge_server.set_state_change("MEDIUM", Constant.LIGHT)
time.sleep(WAIT_TIME)
my_smart_home_edge_server.get_status('', Constant.LIGHT)
time.sleep(WAIT_TIME)

print("\n******************* SETTING UP THE STATUS AND CONTROLLING BY ROOM *******************")
print("\nControlling the devices based on room:")
print("\nCommand ID 20 - my_smart_home_edge_server.set_state_change('HIGH', Constant.LIGHT, 'light_2')")
my_smart_home_edge_server.set('ON', '', '', 'Living') #need to switch on devices before changing its state
time.sleep(WAIT_TIME)
my_smart_home_edge_server.set_state_change("MEDIUM", Constant.LIGHT, '', 'Living')
time.sleep(WAIT_TIME)
my_smart_home_edge_server.set_state_change(30, Constant.AC, '', 'Living')
time.sleep(WAIT_TIME)
my_smart_home_edge_server.get_status('', '', 'Living')
time.sleep(WAIT_TIME)

print("\nCommand ID 21")
my_smart_home_edge_server.set('ON', '', '', 'BR1') #need to switch on devices before changing its state
time.sleep(WAIT_TIME)
my_smart_home_edge_server.set_state_change("HIGH", Constant.LIGHT, '', 'BR1')
time.sleep(WAIT_TIME)
my_smart_home_edge_server.set_state_change(28, Constant.AC, '', 'BR1')
time.sleep(WAIT_TIME)
my_smart_home_edge_server.get_status('', '', 'BR1')
time.sleep(WAIT_TIME)

print("\nControlling the devices based on home:")
print("\nCommand ID 22")
my_smart_home_edge_server.set('ON') #need to switch on devices before changing its state
time.sleep(WAIT_TIME)
my_smart_home_edge_server.set_state_change("MEDIUM", Constant.LIGHT)
time.sleep(WAIT_TIME)
my_smart_home_edge_server.set_state_change(28, Constant.AC)
time.sleep(WAIT_TIME)
my_smart_home_edge_server.get_status()
time.sleep(WAIT_TIME)

print("\n******************* SETTING UP THE STATUS AND CONTROLLING FOR INVALID REQUESTS *******************")
print("\nCommand ID 23")
my_smart_home_edge_server.set_state_change("MEDIUM-HIGH", Constant.LIGHT, "light_2")
time.sleep(WAIT_TIME)

print("\nCommand ID 24")
my_smart_home_edge_server.set_state_change(32, Constant.AC, "AC_BLUE_STAR")
time.sleep(WAIT_TIME)

print("\nCommand ID 25")
my_smart_home_edge_server.set_state_change(32, Constant.AC, "", "Living")
my_smart_home_edge_server.set_state_change("Slow", Constant.LIGHT, "", "Living")
time.sleep(WAIT_TIME)

print("\n******************* CURRENT STATUS BEFORE CLOSING THE PROGRAM *******************")
print("\nCommand ID 26")
my_smart_home_edge_server.get_status()


time.sleep(WAIT_TIME*5)
