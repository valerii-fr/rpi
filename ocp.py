import cv2
import  pyshine as ps
from cv2 import CascadeClassifier
import sys
import numpy
from camera import VideoCamera
import camera
HTML="""
<html>
<head>
<title>PyShine Live Streaming</title>
</head>

<body>
<center><h1> PyShine Live Streaming using OpenCV </h1></center>
<center><img src="stream.mjpg" width='640' height='480' autoplay playsinline></center>
</body>
</html>
"""
def main():
    StreamProps = ps.StreamProps
    StreamProps.set_Page(StreamProps,HTML)
    address = ('192.168.1.102',9000) # Enter your IP address 
    try:
        StreamProps.set_Mode(StreamProps,'cv2')
        strm = camera.get_frame()
        StreamProps.set_Capture(StreamProps, strm)
        StreamProps.set_Quality(StreamProps,90)
        server = ps.Streamer(address,StreamProps)
        print('Server started at','http://'+address[0]+':'+str(address[1]))
        server.serve_forever()
        
    except KeyboardInterrupt:
        capture.release()
        server.socket.close()
        
if __name__=='__main__':
    main()