from evdev import InputDevice, categorize, ecodes
import serial
import time
import json

print("VR BOX Controller test")

#create objects
vrbox = InputDevice('/dev/input/event2')

#controller event codes
btnUp = 273
btnDown = 272
x_var = 0
y_var = 1

#json controller variables
act = 0                         #0 - stop, 1 - left, 2 - right, 3 - forward, 4 - back
spd = 128                       #PWM motor speed control
angle_h = 90                    #laser servo horizontal angle (90 - center)
angle_v = 90                    #laser servo vertical angle (90 - center)
laser_i = 128                   #laser intensity

#json_stop = "{\"act\":0,\"spd\":150,\"angle_v\":90,\"angle_h\":90,\"laser_i\":128} \n"
data_set = {"act":act, "spd":spd, "angle_v":angle_v, "angle_h":angle_h, "laser_i":laser_i}
json = json.dumps(data_set)

for event in vrbox.read_loop():
    if event.type == ecodes.EV_KEY:
        if event.value == 1:
            if event.code == btnUp:
                print("UP")
            elif event.code == btnDown:
                print("DOWN")
                print(json)
    elif event.type == ecodes.EV_REL:
        if event.code == x_var:
            print("X: {x}" .format(x=event.value))
        elif event.code == y_var:
            print("Y: {y}".format(y=event.value))