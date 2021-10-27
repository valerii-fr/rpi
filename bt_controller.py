from evdev import InputDevice, categorize, ecodes
from threading import Timer
import serial
import time
import threading
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
flag = 0

#json_stop = "{\"act\":0,\"spd\":150,\"angle_v\":90,\"angle_h\":90,\"laser_i\":128} \n"
data_set = {"act":act, "spd":spd, "angle_v":angle_v, "angle_h":angle_h, "laser_i":laser_i}
json_str = json.dumps(data_set)
ser = serial.Serial('/dev/ttyS0', 19200, timeout=1)
ser.flush()

def stop_by_timer():
    act = 0
    spd = 0
    data_set = {"act":act, "spd":spd, "angle_v":angle_v, "angle_h":angle_h, "laser_i":laser_i}
    json_str = json.dumps(data_set)
    print(json_str)
    ser.write(str(json_str) .encode('ascii'))
    
def newTimer():
    global timeout_obj
    timeout_obj = Timer(0.1, stop_by_timer)
newTimer()    

for event in vrbox.read_loop():
    if event.type == ecodes.EV_KEY:
        if event.value == 1:
            if event.code == btnUp:
                print("UP")
            elif event.code == btnDown:
                print("DOWN")
                print(json_str)
                act = 0
                spd = 0
                laser_i = 0
                data_set = {"act":act, "spd":spd, "angle_v":angle_v, "angle_h":angle_h, "laser_i":laser_i}
                json_str = json.dumps(data_set)
                print(json_str)
                ser.write(str(json_str) .encode('ascii'))
                time.sleep(0.03)
                laser_i = 255
                data_set = {"act":act, "spd":spd, "angle_v":angle_v, "angle_h":angle_h, "laser_i":laser_i}
                json_str = json.dumps(data_set)
                print(json_str)
                ser.write(str(json_str) .encode('ascii'))
    elif event.type == ecodes.EV_REL:
        timeout_obj.cancel()
        newTimer()
        timeout_obj.start()
        
        if event.code == x_var:
            print("X: {x}" .format(x=event.value))
            if event.value > 0:
                act = 1
                spd = 100 + event.value * 3
                data_set = {"act":act, "spd":spd, "angle_v":angle_v, "angle_h":angle_h, "laser_i":laser_i}
                json_str = json.dumps(data_set)
                print(json_str)
                ser.write(str(json_str) .encode('ascii'))
                timeout_obj.cancel()
                newTimer()
                timeout_obj.start()
            if event.value < 0:
                act = 2
                spd = 100 + event.value * (-3)
                data_set = {"act":act, "spd":spd, "angle_v":angle_v, "angle_h":angle_h, "laser_i":laser_i}
                json_str = json.dumps(data_set)
                print(json_str)
                ser.write(str(json_str) .encode('ascii'))
                timeout_obj.cancel()
                newTimer()
                timeout_obj.start()
        elif event.code == y_var:
            print("Y: {y}".format(y=event.value))
            if event.value < 0:
                act = 3
                spd = 64 + event.value * (-5)
                data_set = {"act":act, "spd":spd, "angle_v":angle_v, "angle_h":angle_h, "laser_i":laser_i}
                json_str = json.dumps(data_set)
                print(json_str)
                ser.write(str(json_str) .encode('ascii'))
                timeout_obj.cancel()
                newTimer()
                timeout_obj.start()
            if event.value > 0:
                act = 4
                spd = 64 + event.value * 5
                data_set = {"act":act, "spd":spd, "angle_v":angle_v, "angle_h":angle_h, "laser_i":laser_i}
                json_str = json.dumps(data_set)
                print(json_str)
                ser.write(str(json_str) .encode('ascii'))
                timeout_obj.cancel()
                newTimer()
                timeout_obj.start()