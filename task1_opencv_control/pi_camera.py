import cv2
from picamera.array import PiRGBArray
from picamera import PiCamera

class Camera(object):
    def __init__(self):
        self.camera = True
        print("Starting pi camera")

    def get_frame(self):
        camera = PiCamera()
        camera.resolution = (640, 480)
        camera.framerate = 32 
        capture = PiRGBArray(camera, size=(640, 480))
        camera.capture(capture, format="bgr")
        frame = capture.array
        result = cv2.imencode('.jpg', frame)[1].tobytes()
        camera.close()
        return result
