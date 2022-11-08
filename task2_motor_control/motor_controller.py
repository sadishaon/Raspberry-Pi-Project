try:
    from .fake_gpio import GPIO  # For running app
except ImportError:
    from fake_gpio import GPIO   # For running main

#import RPi.GPIO as GPIO # For testing in Raspberry Pi

import random
import time

class MotorController(object):
  def __init__(self):
    self.working = False
    

  def start_motor(self):
    self.PIN_STEP = 25     # do not change
    self.PIN_DIR = 8       # do not change
    self.working = True
    
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(self.PIN_DIR, GPIO.OUT)
    GPIO.setup(self.PIN_STEP, GPIO.OUT)
    print('Motor started')

    cw  = 0           # Clockwise initialization
    ccw = 1           # Counterclockwise initialization
    SPR = 1600        # Motor roartes 0.225° pre steps (360°/0.225° = 1600 total steps)

    # For spinning 90° or 270°
    step_count_1 = int(SPR / 4)      #      = 400   For 90° degree rotation
    step_count_2 = int(SPR * (3/4))  #      = 1200  For 270° degree rotation
    delay = 0.005

    # For choose randomly, whether the motor should to rotate 90° or 270° 
    steps = [step_count_1, step_count_2]
    random_steps = random.choice(steps)

    # For choose randomly, whether it should rotate clockwise or counterclockwise
    directions = [cw, ccw]
    random_directions = random.choice(directions)

    while self.working:
      GPIO.output(self.PIN_DIR, random_directions)
      for x in range(random_steps):
        while self.working == True:

          if random_directions == cw and random_steps == step_count_1:
            print('Rotating 90° degrees in clockwise direction')
            
          elif random_directions == cw and random_steps == step_count_2:
            print('Rotating 270 degrees in clockwise direction')
            
          elif random_directions == ccw and random_steps == step_count_1:
            print('Rotating 90° degrees in counter-clockwise direction')
            
          elif random_directions == ccw and random_steps == step_count_2:
            print('Rotating 270° degrees in counter-clockwise direction')
            
          GPIO.output(self.PIN_STEP, True)
          time.sleep(delay)
          GPIO.output(self.PIN_STEP, False)
          time.sleep(delay)
        break

  def motor_stopped(self):
    self.working = False
    return self.working

  def is_working(self):
    return self.working