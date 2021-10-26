import serial
import time
import json

ser = serial.Serial('/dev/ttyS0', 19200, timeout=1)
ser.flush()

json_data = "{\"act\":1,\"spd\":128,\"angle_v\":90,\"angle_h\":90,\"laser_i\":128} \n"
    
json_data2 = "{\"act\":0,\"spd\":128,\"angle_v\":90,\"angle_h\":90,\"laser_i\":128} \n"
    
while True:
    str1 = ser.write(str(json_data) .encode('ascii'))
    print(str1)
    time.sleep(0.25)
    str1 = ser.write(str(json_data2) .encode('ascii'))
    print(str1)
    time.sleep(0.25)