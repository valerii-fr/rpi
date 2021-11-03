#!/usr/bin/env python
import cv2
face_cascade = cv2.CascadeClassifier('/home/pi/downloads/opencv-master/data/haarcascades/haarcascade_frontalface_default.xml')
class VideoCamera(object):
    def __init__(self):
        # Using OpenCV to capture from device 0. If you have trouble capturing
        # from a webcam, comment the line below out and use a video file
        # instead.
        self.video = cv2.VideoCapture(0)
        self.video.set(cv2.CAP_PROP_BUFFERSIZE,4)
        self.video.set(cv2.CAP_PROP_FRAME_WIDTH,640)
        self.video.set(cv2.CAP_PROP_FRAME_HEIGHT,480)
        self.video.set(cv2.CAP_PROP_FPS,30)
        
        # If you decide to use video.mp4, you must have this file in the folder
        # as the main.py.
        # self.video = cv2.VideoCapture('video.mp4')
    
    def __del__(self):
        self.video.release()
    
    def get_frame(self):
        success, image = self.video.read()
        # We are using Motion JPEG, but OpenCV defaults to capture raw images,
        # so we must encode it into JPEG in order to correctly display the
        # video stream.
        faces = face_cascade.detectMultiScale(image, 1.3, 5)
        for (x, y, w, h) in faces:
            cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2)
            cv2.putText(image, x, (20,20), cv2.FONT_HERSHEY_SIMPLEX, 1, color_yellow, 2)
            cv2.putText(image, y, (20,40), cv2.FONT_HERSHEY_SIMPLEX, 1, color_yellow, 2)
        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()