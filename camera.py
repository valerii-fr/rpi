#!/usr/bin/env python
import cv2
from threading import Timer
import serial
import time
import threading
import json

face_cascade = cv2.CascadeClassifier('/home/pi/downloads/opencv-master/data/haarcascades/haarcascade_frontalface_default.xml')
color_yellow = (0,255,255)
act = 0                         #0 - stop, 1 - left, 2 - right, 3 - forward, 4 - back
spd = 128                       #PWM motor speed control
angle_h = 90                    #laser servo horizontal angle (90 - center)
angle_v = 90                    #laser servo vertical angle (90 - center)
laser_i = 0                   #laser intensity

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

class VideoCamera(object):      
    def __init__(self):
        # Using OpenCV to capture from device 0. If you have trouble capturing
        # from a webcam, comment the line below out and use a video file
        # instead.
        self.video = cv2.VideoCapture(0)
        self.video.set(cv2.CAP_PROP_BUFFERSIZE,4)
        self.video.set(cv2.CAP_PROP_FRAME_WIDTH,320)
        self.video.set(cv2.CAP_PROP_FRAME_HEIGHT,240)
        self.video.set(cv2.CAP_PROP_FPS,30)
        
        # If you decide to use video.mp4, you must have this file in the folder
        # as the main.py.
        # self.video = cv2.VideoCapture('video.mp4')
    
    def __del__(self):
        self.video.release()
    
    def get_frame(self):
        timeout_obj.cancel()
        newTimer()
        timeout_obj.start()
        
        success, image = self.video.read()
        # We are using Motion JPEG, but OpenCV defaults to capture raw images,
        # so we must encode it into JPEG in order to correctly display the
        # video stream.
        faces = face_cascade.detectMultiScale(image, 1.3, 5)
        for (x, y, w, h) in faces:
            cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2)
            cv2.putText(image, str(x), (0,20), cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.5, color_yellow, 1)
            cv2.putText(image, str(y), (0,40), cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.5, color_yellow, 1)
            if x < 80:
                act = 1
                spd = 150
                data_set = {"act":act, "spd":spd, "angle_v":angle_v, "angle_h":angle_h, "laser_i":laser_i}
                json_str = json.dumps(data_set)
                print(json_str)
                ser.write(str(json_str) .encode('ascii'))
                timeout_obj.cancel()
                newTimer()
                timeout_obj.start()
            if x > 240:
                act = 2
                spd = 150
                data_set = {"act":act, "spd":spd, "angle_v":angle_v, "angle_h":angle_h, "laser_i":laser_i}
                json_str = json.dumps(data_set)
                print(json_str)
                ser.write(str(json_str) .encode('ascii'))
                timeout_obj.cancel()
                newTimer()
                timeout_obj.start()
        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()