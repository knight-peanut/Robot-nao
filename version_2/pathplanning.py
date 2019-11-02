from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

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

#IP = "192.168.43.35"
IP = "192.168.43.195"

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

visualBasis = VisualBasis(IP,cameraId=0, resolution=vd.kVGA)
ballDetect = BallDetect(IP, resolution=vd.kVGA, writeFrame=True)
stickDetect = StickDetect(IP, cameraId=0, resolution=vd.kVGA, writeFrame=True)
landMarkDetect = LandMarkDetect(IP)
MotionBasis = NewMotionBasis(IP)

motionProxy = ALProxy("ALMotion", IP, 9559)
postureProxy = ALProxy("ALRobotPosture", IP, 9559)
motionProxy.wakeUp()

postureProxy.goToPosture("StandInit", 0.2)


def TriangleCalculation(x,s,alpha):
    if (alpha < 0.0):
        alpha = abs(alpha)
        l2 = x*x + s*s - 2*x*s*math.cos(alpha)
        l = math.sqrt(l2)
        costheta = (x*x + l2 - s*s)/(2*x*l)
        theta = math.acos(costheta)
        if theta >= math.pi/2:
            theta2 = theta - math.pi/2
            turnAngle1 = theta2
            dis1 = 0 - x*math.sin(theta2)
            turnAngle2 = 0
            dis2 = x*math.cos(theta2)-0.15 

        if theta < math.pi/2:
            theta2 = math.pi/2 - theta
            turnAngle1 = 0 - theta2
            dis1 = x*math.cos(theta)           
            turnAngle2 = 0
            dis2 = x*math.sin(theta)-0.15

        
        turndata = [dis1,dis2,turnAngle1,turnAngle2]
        return turndata
    if (alpha > 0.0):
        l2 = x*x + s*s - 2*x*s*math.cos(alpha)
        l = math.sqrt(l2)
        costheta = (x*x + l2 - s*s)/(2*x*l)
        theta = math.acos(costheta)
        if theta >= math.pi/2:
            theta2 = theta - math.pi/2
            turnAngle1 = 0 - theta2
            dis1 = x*math.sin(theta2)+0.02 
            turnAngle2 = 0
            dis2 = x*math.cos(theta2)-0.15


        if theta < math.pi/2:
            theta2 = math.pi/2 - theta
            turnAngle1 = theta2
            dis1 = -x*math.cos(theta)- 0.02
            turnAngle2 = 0
            dis2 = x*math.sin(theta)-0.15
        
        turndata = [dis1,dis2,turnAngle1,turnAngle2]
        return turndata  

def KeepDis():
    
    
    for i in range(3):
        ballDetect.CrouchingHeadSearching()
        y=ballDetect.getBallPosition()[1]
        ballDetect.showBallPosition()
        flag=0
        while abs(y)>=0.1 and flag<2:
            print('y overflow, refreshing searching redball!')
            
            ballDetect.CrouchingHeadSearching()
            y=ballDetect.getBallPosition()[1]
            ballDetect.showBallPosition()
            flag+=1
        
        motionProxy.moveTo(0,y,0,moveConfig)

    #motionProxy.moveTo(0,0.02,0,[['MaxStepFrequency',0.5],['StepHeight',0.01]])

    ballDetect.CrouchingHeadSearching()
    
    x=ballDetect.getBallPosition()[0]

    if(not ballDetect.RedballIsInSight()):
        x=0.15

    ballDetect.showBallPosition()

    landMarkDetect.updateLandMarkData()
    landMarkDetect.showLandMarkData()
    markdata=landMarkDetect.getLandMarkData()

    if(not landMarkDetect.landmarkIsInSight()):
        time.sleep(2.0)
        landMarkDetect.updateLandMarkData()
        landMarkDetect.showLandMarkData()
        markdata=landMarkDetect.getLandMarkData()
        
    if(landMarkDetect.landmarkIsInSight()):
        
        s=markdata[2]
        alpha = markdata[3]
        turndata = TriangleCalculation(x,s,alpha)

        motionProxy.setMoveArmsEnabled(False, False)
        motionProxy.moveTo(0.0,0.0,turndata[2],moveConfig)


        motionProxy.setMoveArmsEnabled(False, False)
        motionProxy.moveTo(0.0,0.0,turndata[3],moveConfig)


    ballDetect.CrouchingHeadSearching()
    x=ballDetect.getBallPosition()[0]

    ballDetect.showBallPosition()
    
    while(x>=0.3):
        motionProxy.moveTo(0.05,0,0,moveConfig)
        ballDetect.CrouchingHeadSearching()
        x=ballDetect.getBallPosition()[0]

        ballDetect.showBallPosition()

    for i in range(4):
        ballDetect.CrouchingHeadSearching()
        x=ballDetect.getBallPosition()[0]

        ballDetect.showBallPosition()
        
        if(x>=0.15):
            motionProxy.moveTo(0.05,0,0,moveConfig)
    
    motionProxy.moveTo(x-0.1,0,0,moveConfig)
    
    ballDetect.CrouchingHeadSearching()
    y=ballDetect.getBallPosition()[1]
    ballDetect.showBallPosition()
    if y>-0.02:
        motionProxy.moveTo(0.0,y-(-0.04),0.0,moveConfig)

    '''
    ballDetect.CrouchingHeadSearching()
    x=ballDetect.getBallPosition()[0]

    ballDetect.showBallPosition()

    landMarkDetect.updateLandMarkData()
    landMarkDetect.showLandMarkData()
    markdata=landMarkDetect.getLandMarkData()
    s=markdata[2]
    alpha = markdata[3]
    turndata = TriangleCalculation(x,s,alpha)
    motionProxy.setMoveArmsEnabled(False, False)
    motionProxy.moveTo(0.0,0.0,turndata[2],[['MaxStepFrequency',0.3],['StepHeight',0.01]])


    motionProxy.setMoveArmsEnabled(False, False)
    motionProxy.moveTo(0.0,0.0,turndata[3],[['MaxStepFrequency',0.3],['StepHeight',0.01]])
    '''
    

def KeepDis_task3():

    '''
    for i in range(3):
        ballDetect.CrouchingHeadSearching()
        y=ballDetect.getBallPosition()[1]
        motionProxy.moveTo(0,y,0,[['MaxStepFrequency',0.3],['StepHeight',0.01]])

    #motionProxy.moveTo(0,0.02,0,[['MaxStepFrequency',0.3],['StepHeight',0.01]])
    '''
   

    ballDetect.CrouchingHeadSearching()
    x=ballDetect.getBallPosition()[0]
    y=ballDetect.getBallPosition()[1]
    motionProxy.moveTo(0,y,0,moveConfig)
    ballDetect.showBallPosition()
    while(x>=0.3):
        motionProxy.moveTo(0.05,0,0,moveConfig)
        ballDetect.CrouchingHeadSearching()
        x=ballDetect.getBallPosition()[0]
        ballDetect.showBallPosition()

    for i in range(4):
        ballDetect.CrouchingHeadSearching()
        x=ballDetect.getBallPosition()[0]
        ballDetect.showBallPosition()
        if(x>=0.15):
            motionProxy.moveTo(0.05,0,0,moveConfig)
            
    ballDetect.CrouchingHeadSearching()
    x=ballDetect.getBallPosition()[0]
    y=ballDetect.getBallPosition()[1]
    ballDetect.showBallPosition()
    motionProxy.moveTo(x-0.1,0,0,moveConfig)

    time.sleep(2.0)

    motionProxy.moveTo(0,y-(-0.04),0,moveConfig)

    time.sleep(1.0)

    print('speAngle start')
    speAngle=ballDetect.getspeAngle()
    motionProxy.moveTo(0,0,-speAngle,moveConfig)
    #time.sleep(1.0)
            
