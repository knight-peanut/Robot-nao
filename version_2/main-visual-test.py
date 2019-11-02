"""
some test codes for Nao golf visual part.
@author: Meringue
@date: 2018/1/15
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from PIL import Image

import numpy as np
import cv2
import time
import os
import sys
#sys.path.append("/home/meringue/Softwares/pynaoqi-sdk/") #naoqi directory
sys.path.append("./")

from action import *
from visualTask import *
from naoqi import ALProxy
import vision_definitions as vd

IP = "192.168.43.114"


visualBasis = VisualBasis(IP,cameraId=0, resolution=vd.kVGA)
ballDetect = BallDetect(IP, resolution=vd.kVGA, writeFrame=True)
stickDetect = StickDetect(IP, cameraId=0, resolution=vd.kVGA, writeFrame=True)
landMarkDetect = LandMarkDetect(IP)
MotionBasis = MotionBasis(IP)

# test code
"""
visualBasis.updateFrame()
visualBasis.showFrame()
visualBasis.printFrameData()
cv2.waitKey(1000)
"""

# posture initialization
motionProxy = ALProxy("ALMotion", IP, 9559)
postureProxy = ALProxy("ALRobotPosture", IP, 9559)
motionProxy.wakeUp()

postureProxy.goToPosture("StandInit", 0.2)



'''
def getImage(IP, PORT, cameraID):
        
        
    camProxy = ALProxy("ALVideoDevice", IP, 9559)
    # vision_definitions.kCameraSelectID = vision_definitions.kBottomCamera ，以前的API写法，使用底部摄像头
    camProxy.setActiveCamera(cameraID) 
    if (cameraID == 0):  # Bottom Camera
        camProxy.setCameraParameter("test", 18, 0)
    elif (cameraID == 1):  # Top Camera
        camProxy.setCameraParameter("test", 18, 1)

    resolution = vd.kVGA  # 定义resolution
    colorSpace = vd.kRGBColorSpace  # 定义色域
    fps = 15

    nameId = camProxy.subscribe("test", resolution, colorSpace, fps)  # 使用Borker订阅模块
    naoImage = camProxy.getImageRemote(nameId)  # 获取当前图片

    imageWidth = naoImage[0]
    imageHeight = naoImage[1]

    array = naoImage[6]
    im = Image.frombytes("RGB", (imageWidth, imageHeight), array)

    im.save("D:\\camImage.png", "PNG")  # 临时图片路径
    
    camProxy.unsubscribe(nameId)

name =['HeadPitch','HeadYaw']
angle = [-13.7*almath.TO_RAD,1.0*almath.TO_RAD]
fractionMaxSpeed = 0.2
motionProxy.setAngles(name,angle,fractionMaxSpeed)
getImage(IP,9559,1)
'''

ballDetect.CrouchingHeadSearching()
ballDetect.sliderHSV(client="test3")        





'''
while 1:
	stickDetect.updateStickData(client="xxx")
	stickDetect.showStickPosition()
	cv2.waitKey(0)

'''

"""
print "start collecting..."
for i in range(10):
	imgName = "stick_" + str(i+127) + ".jpg"
	imgDir = os.path.join("stick_images", imgName)
	visualBasis.updateFrame()
	visualBasis.showFrame(timeMs=1000)
	visualBasis.saveFrame(imgDir)
	print "saved in ", imgDir
	time.sleep(5)
"""

"""
visualBasis._tts.say("hello world")
"""

"""
visualBasis._motionProxy.wakeUp()
"""

"""
dataList = visualBasis._memoryProxy.getDataList("camera")
print dataList
"""

"""
visualBasis._motionProxy.setStiffnesses("Body", 1.0)
visualBasis._motionProxy.moveInit()

"""



