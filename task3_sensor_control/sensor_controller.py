try:
    from .fake_gpio import GPIO # For running app
except ImportError:
    from fake_gpio import GPIO  # For running main

#import RPi.GPIO as GPIO

import time
import numpy as np
import random

class SensorController(object):
    
    def __init__(self):
        self.PIN_TRIGGER = 18 # do not change
        self.PIN_ECHO = 24 # do not change
        self.distance = None
        self.color_from_distance = [False,False,False]
        print('Sensor controller initiated')

    def track_rod(self):  
    # Initalization of end and start time
        start = 0
        end = 0
        values = []
        loop = True

        while loop:
            GPIO.setmode(GPIO.BCM)                   # Using BCM numbers
            GPIO.setup(self.PIN_TRIGGER, GPIO.OUT)   # Setup trigger pin as output to start the sensor
            GPIO.setup(self.PIN_ECHO, GPIO.IN)       # Set echo pin to receive input

            GPIO.output(self.PIN_TRIGGER, False)     # Set trigger pin to low to let the sensor settle
            time.sleep(0.1)

            GPIO.output(self.PIN_TRIGGER, True)      # Set pin trigger to high to allow sensor to trigger
            time.sleep(0.00001)                      # Wait 10 micro second

            GPIO.output(self.PIN_TRIGGER, False)

            while GPIO.input(self.PIN_ECHO) == 0:    # Wait till ECHO is Low (start time)
                start = time.time()

            while GPIO.input(self.PIN_ECHO) == 1:    # Wait till ECHO is High (end time)
                end = time.time()

            duration = end - start
            self.distance =  14 #np.round(17150*duration, 2)

            #print('Distance in cm : ', self.distance)

            values.append(self.distance)              # Add distance to list
            #print ('List : ', values)
        
            if len(values) > 20:
                loop = False
                median = np.median(values)
                #print ('Median', median)
                self.distance = median
                del values[0]

            # Color zone based on distance measure

            if(self.distance >= 4 and self.distance <= 8.5):
                self.color_from_distance = [False,False,True]
                #print('Yellow Color Zone')

            elif(self.distance >= 8.6 and self.distance <= 10.5):
                self.color_from_distance = [False,True,True]
                #print('Yellow Color and Purple Color Zone')

            elif(self.distance >= 10.6 and self.distance <= 13.5):
                self.color_from_distance = [False,True,False]
                #print('Purple Color Zone')

            elif(self.distance >= 13.6 and self.distance <= 15.5):
                self.color_from_distance = [True,True,False]
                #print('Purple Color and Green Color Zone')
            
            elif(self.distance >= 15.6 and self.distance <= 19):
                self.color_from_distance = [True,False,False]
                #print('Green Color Zone')

            elif(self.distance < 4 or self.distance > 19):
                self.color_from_distance = [False,False,False]
                #print('Outside of Color Zone')


            print('Distance in cm : ', self.distance)
            GPIO.cleanup()
            print ('Monitoring')


    def get_distance(self):
        return self.distance

    def get_color_from_distance(self):
        return self.color_from_distance
