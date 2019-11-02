
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from pathplanning import *

import numpy as np
import cv2
import time
import os
import sys
import thread
#sys.path.append("/home/meringue/Softwares/pynaoqi-sdk/") #naoqi directory
sys.path.append("./")

from newaction import *
from visualTask import *
from naoqi import ALProxy
import vision_definitions as vd

IP = "192.168.43.195"
#IP = "192.168.43.35"

visualBasis = VisualBasis(IP,cameraId=0, resolution=vd.kVGA)
ballDetect = BallDetect(IP, resolution=vd.kVGA, writeFrame=True)
stickDetect = StickDetect(IP, cameraId=0, resolution=vd.kVGA, writeFrame=True)
landMarkDetect = LandMarkDetect(IP)
MotionBasis = NewMotionBasis(IP)

motionProxy = ALProxy("ALMotion", IP, 9559)
postureProxy = ALProxy("ALRobotPosture", IP, 9559)
motionProxy.wakeUp()

postureProxy.goToPosture("StandInit", 0.2)
            
 
maxstepx = 0.04
maxstepy = 0.14
maxsteptheta = 0.4
maxstepfrequency = 0.6
stepheight = 0.02
torsowx = 0.0
torsowy = 0.0
moveConfig = [["MaxStepX",maxstepx],
            ["MaxStepY",maxstepy],
            ["MaxStepTheta",maxsteptheta],
            ["MaxStepFrequency",maxstepfrequency],
            ["StepHeight",stepheight],
            ["TorsoWx",torsowx],
            ["TorsoWy",torsowy]]
motionProxy.setMoveArmsEnabled(False, False)

thread.start_new_thread(MotionBasis.LoseHand,())
MotionBasis.GrabRod()
MotionBasis.CloseRod()
time.sleep(2.0)


MotionBasis.headtouch()
time.sleep(2.0)


MotionBasis.HitBall(0.07)
time.sleep(2.0)
MotionBasis.CloseRod()
time.sleep(1.0)



motionProxy.moveTo(0,0,-90*almath.TO_RAD,moveConfig)

time.sleep(1.0)

for i in range(4):
    motionProxy.moveTo(0.20,0,0,moveConfig)
    time.sleep(1.0)
motionProxy.moveTo(0,0,-10*almath.TO_RAD,moveConfig)

time.sleep(2.0)

ballDetect.NewSearchingRedBall_task3()
x,y,angle = ballDetect.getBallPosition()
print ('111111111111111111111111111111')
while x==0 and y==0 and angle==0:
    
    name =['HeadPitch','HeadYaw']
    targetangle = [-0.4*almath.TO_RAD,0.0*almath.TO_RAD]
    fractionMaxSpeed = 0.2
    print ('here!')
    motionProxy.angleInterpolationWithSpeed(name,targetangle,fractionMaxSpeed)
    motionProxy.moveTo(0.2,0,0,moveConfig)
    ballDetect.NewSearchingRedBall_task3()
    x,y,angle = ballDetect.getBallPosition()

print ('222222222222222222222222222222')



KeepDis_task3()
time.sleep(2.0)

MotionBasis.HitBall(0.2)
time.sleep(2.0)
MotionBasis.CloseRod()
time.sleep(1.0)




MotionBasis.headtouch()
time.sleep(2.0)

#击球后转身直走
motionProxy.moveTo(0,0,-90*almath.TO_RAD,moveConfig)
time.sleep(2.0)
for i in range(4):
    motionProxy.moveTo(0.5,0,0,moveConfig)
    time.sleep(2.0)

#找球找球洞
ballDetect.SearchingRedBall()
x,y,angle = ballDetect.getBallPosition()
while x==0 and y==0 and angle==0:
    
    name =['HeadPitch','HeadYaw']
    targetangle = [-0.4*almath.TO_RAD,0.0*almath.TO_RAD]
    fractionMaxSpeed = 0.2
    motionProxy.angleInterpolationWithSpeed(name,targetangle,fractionMaxSpeed)
    motionProxy.moveTo(0.3,0,0,[['MaxStepFrequency',0.5],['StepHeight',0.01]])
    ballDetect.SearchingRedBall()
    x,y,angle = ballDetect.getBallPosition()


time.sleep(1.0)
ballDetect.CrouchingHeadSearching()
x=ballDetect.getBallPosition()[0]

landMarkDetect.updateLandMarkData()
landMarkDetect.showLandMarkData()
markdata=landMarkDetect.getLandMarkData()
s=markdata[2]
alpha = markdata[3]

MotionBasis.setalpha(alpha)

turndata = TriangleCalculation(x,s,alpha)
name =['HeadPitch','HeadYaw']
targetangle = [-0.4*almath.TO_RAD,0.0*almath.TO_RAD]
fractionMaxSpeed = 0.2
motionProxy.angleInterpolationWithSpeed(name,targetangle,fractionMaxSpeed)
MotionBasis.AdjustPosition(turndata)

time.sleep(1.0)

KeepDis()

time.sleep(2.0)
MotionBasis.HitBall(0.2)
time.sleep(2.0)
MotionBasis.CloseRod()
time.sleep(1.0)



