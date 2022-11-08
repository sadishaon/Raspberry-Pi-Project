try:
    from .camera import Camera # For running app
except ImportError:
    from camera import Camera # For running main

#from task1_opencv_control.pi_camera import Camera # For Raspberry Pi

import cv2
import numpy as np

class OpenCVController(object):

    def __init__(self):
        self.current_color = [False,False,False]
        self.camera = Camera()
        print('OpenCV controller initiated')

    def process_frame(self):
        frame = self.camera.get_frame()
        frame = np.frombuffer(frame,np.uint8)

        # RGB to BGR Conversion
        frame = cv2.imdecode(frame, cv2.COLOR_RGB2BGR)

        # BGR to HSV
        frame_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Red
        lower_red = np.array([160, 20, 70])
        upper_red = np.array([190, 255, 255])
        red_mask  = cv2.inRange(frame_hsv, lower_red, upper_red)

        # Green
        green_lower = np.array([30, 40, 70])
        green_upper = np.array([50, 255, 255])
        green_mask  = cv2.inRange(frame_hsv, green_lower, green_upper)

        # Yellow
        yellow_lower = np.array([15, 150, 20])
        yellow_upper = np.array([35, 255, 255])
        yellow_mask  = cv2.inRange(frame_hsv, yellow_lower, yellow_upper)

        # Purple
        purple_lower = np.array([129, 50, 70])
        purple_upper = np.array([158, 255, 255])
        purple_mask  = cv2.inRange(frame_hsv, purple_lower, purple_upper)
        
        kernal = np.ones((5, 5), "uint8")

        # Red mask
        red_mask = cv2.dilate(red_mask, kernal)
        #red = cv2.bitwise_and(frame, frame, mask=red_mask)

        # Green mask
        green_mask = cv2.dilate(green_mask, kernal)
        #green = cv2.bitwise_and(frame, frame, mask = green_mask)

        # Yellow mask
        yellow_mask = cv2.dilate(yellow_mask, kernal)
        #yellow = cv2.bitwise_and(frame, frame, mask = yellow_mask)

        # Purple mask
        purple_mask = cv2.dilate(purple_mask, kernal)
        #purple = cv2.bitwise_and(frame, frame, mask = purple_mask)


        # Red Mark Detection
        contours, hierarchy = cv2.findContours(red_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for contour in contours:
            area = cv2.contourArea(contour)
            if(area > 5000):
                xr, yr, wr, hr = cv2.boundingRect(contour)
                imageFrame = cv2.rectangle(frame, (xr, yr),(xr+wr, yr+hr), (0, 0, 255), 3) # colour of border
                cv2.putText(imageFrame, "Mark", (xr, yr),cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255))
                l11 = (xr, yr)
                l12 = (xr+wr, yr+hr)


        # Green Mark Detection
        contours, hierarchy=cv2.findContours(green_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for contour in contours:
            area = cv2.contourArea(contour)
            if(area > 20000):
                xg, yg, wg, hg = cv2.boundingRect(contour)
                imageFrame = cv2.rectangle(frame, (xg, yg),(xg+wg, yg+hg), (0, 255, 0), 3) # colour of border
                cv2.putText(imageFrame, "Green", (xg, yg),cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0))
                l21 = (xg,yg)
                l22 = (xg+wg, yg+hg)
                
        # purple Mark Detection
        contours, hierarchy=cv2.findContours(purple_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for contour in contours:
            area = cv2.contourArea(contour)
            if (area > 5000):
                xp, yp, wp, hp = cv2.boundingRect(contour)
                imageFrame = cv2.rectangle(frame, (xp, yp),(xp+wp, yp+hp), (255, 0, 255), 3) # colour of border
                cv2.putText(imageFrame, "Purple", (xp, yp),cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 0, 255))
                l31 = (xp, yp)
                l32 = (xp+wp, yp+hp)


        # Yellow Mark Detection
        contours, hierarchy=cv2.findContours(yellow_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for contour in contours:
            area = cv2.contourArea(contour)
            if(area > 8000):
                xy, yy, wy, hy = cv2.boundingRect(contour)
                imageFrame = cv2.rectangle(frame, (xy, yy),(xy+wy, yy+hy), (0, 255, 255), 3) # colour of border
                cv2.putText(imageFrame, "Yellow", (xy, yy),cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 255))
                l41 = (xy, yy)
                l42 = (xy+wy, yy+hy)
                
                        
        # From Left side to Right side

        if ((l21 <= l11 < l22) and (l21 <= l12 < l22) or ((l11 < l21) and (l12 < l22))):
            self.current_color = [True,False,False]
        if ((l21 <= l11 < l22) and (l31 <= l12 < l32)):
            self.current_color = [True,True,False]
        if ((l31 <= l11 < l32) and (l31 <= l12 < l32)):
            self.current_color = [False,True,False]
        if ((l31 <= l11 < l32) and (l41 <= l12 <= l42)):
            self.current_color = [False,True,True]
        if ((l41 <= l11 <= l42) and (l41 <= l12 <= l42)):
            self.current_color = [False,False,True]

        # From Right side to Left side

        if ((l21 >= l11 > l22) and (l21 >= l12 > l22)):
            self.current_color = [True,False,False]
        if ((l21 >= l11 > l22) and (l31 >= l12 > l32)):
            self.current_color = [True,True,False]
        if ((l31 >= l11 > l32) and (l31 >= l12 > l32)):
            self.current_color = [False,True,False]
        if ((l31 >= l11 > l32) and (l41 >= l12 >= l42)):
            self.current_color = [False,True,True]
        if ((l41 >= l11 >= l42) and (l41 >= l12 >= l42)):
            self.current_color = [False,False,True] 

        ret,buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        print('Monitoring')
        return frame

    def get_current_color(self):
        return self.current_color
