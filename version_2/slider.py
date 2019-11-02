"""
This code is used to adjust some key parameters related to
red ball and yellow stick detection in golf task.
@author: Meringue
@date: 2018/10/15
"""

import cv2
import numpy as np
from visualTask import *
from naoqi import ALProxy
import vision_definitions as vd

if __name__ == "__main__":
    IP = "192.168.43.114"
    # for ball detection
    motionProxy = ALProxy("ALMotion", IP, 9559)
    postureProxy = ALProxy("ALRobotPosture", IP, 9559)
    motionProxy.wakeUp()

    postureProxy.goToPosture("StandInit", 0.2)
    detector = BallDetect(IP, resolution=vd.kVGA)
    detector.sliderHSV(client="test3")

    # for stick detection
    #detector = StickDetect(IP)
    #detector.slider(client = "test2")
