from naoqi import ALProxy
import sys
sys.path.append(r'/home/nao/pynaoqi')
import almath
import time
import math
import motion
import thread
from PIL import Image
import cv2
import numpy as np

robotIP="127.0.0.1"
PORT=9559

AutoProxy=ALProxy("ALAutonomousLife",robotIP,PORT)
memoryProxy = ALProxy("ALMemory", robotIP ,PORT)        
motionPrx = ALProxy("ALMotion", robotIP , PORT)      
tts = ALProxy("ALTextToSpeech", robotIP, PORT)
postureProxy = ALProxy("ALRobotPosture", robotIP , PORT)
memoryProxy = ALProxy("ALMemory", robotIP , PORT)
redballProxy = ALProxy("ALRedBallDetection", robotIP , PORT)
camProxy = ALProxy("ALVideoDevice", robotIP, PORT)
landmarkProxy = ALProxy("ALLandMarkDetection", robotIP, PORT)

PositionJointNamesR  = ["RShoulderPitch", "RShoulderRoll", "RElbowYaw", "RElbowRoll", "RWristYaw","RHand"]
golfPositionJointAnglesR1  = [1.01402, 0.314159, 1.62907, 1.48035, -0.648924,  0.12]
golfPositionJointAnglesR2  = [1.02629, 0.314159, 1.62907, 1.48342, 0.230058, 0.12]
golfPositionJointAnglesR3  = [1.03549, 0.314159, 1.64747, 0.998676, 0.476658,  0.12]
golfPositionJointAnglesR4  = [1.03549, 0.314159, 1.66742, 0.971064, -0.980268, 0.12]
golfPositionJointAnglesR5  = [1.07998, 0.314159, 1.61986, 1.11679, 0.082794, 0.6]  
golfPositionJointAnglesR6  = [1.07998, 0.314159, 1.61986, 1.11679, 0.082794, 0.12]  


stop1=0
landmarkFlag = 0
redballFlag = 0    

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


def zhuagan():
    while True:
        RighthandTouchedFlag = memoryProxy.getData("HandRightRightTouched")
        if RighthandTouchedFlag == 1.0:
            print "right hand touched"
            tts.say("give me a club ")
            motionPrx.angleInterpolationWithSpeed(PositionJointNamesR,golfPositionJointAnglesR5,0.4);
            time.sleep(4)
            motionPrx.angleInterpolationWithSpeed(PositionJointNamesR,golfPositionJointAnglesR6,0.4);
            
            time.sleep(1)
            motionPrx.angleInterpolationWithSpeed(PositionJointNamesR,golfPositionJointAnglesR2,0.4)
            motionPrx.angleInterpolationWithSpeed(PositionJointNamesR,golfPositionJointAnglesR3,0.4)
            time.sleep(3)
            motionPrx.angleInterpolationWithSpeed(PositionJointNamesR,golfPositionJointAnglesR4,0.12)
            break

def headtouch():
    while True:
        headTouchedButtonFlag = memoryProxy.getData("FrontTactilTouched")
        if headTouchedButtonFlag == 1.0:
            print "front head touched"
            tts.say("begin the round three")
            break

def HitBall():
    
    if (alpha<0):
        motionPrx.angleInterpolationWithSpeed(PositionJointNamesR,golfPositionJointAnglesR1,0.4)
        motionPrx.angleInterpolationWithSpeed(PositionJointNamesR,golfPositionJointAnglesR2,0.4)
        motionPrx.angleInterpolationWithSpeed(PositionJointNamesR,golfPositionJointAnglesR3,0.4)
        time.sleep(3)
        motionPrx.angleInterpolationWithSpeed(PositionJointNamesR,golfPositionJointAnglesR4,0.20)
        time.sleep(2)
        motionPrx.angleInterpolationWithSpeed(PositionJointNamesR,golfPositionJointAnglesR1,0.4)
    if (alpha>0):
        motionPrx.angleInterpolationWithSpeed(PositionJointNamesR,golfPositionJointAnglesR2,0.4)
        motionPrx.angleInterpolationWithSpeed(PositionJointNamesR,golfPositionJointAnglesR1,0.4)
        motionPrx.angleInterpolationWithSpeed(PositionJointNamesR,golfPositionJointAnglesR4,0.4)
        time.sleep(3)
        motionPrx.angleInterpolationWithSpeed(PositionJointNamesR,golfPositionJointAnglesR3,0.12)
        time.sleep(2)
        motionPrx.angleInterpolationWithSpeed(PositionJointNamesR,golfPositionJointAnglesR1,0.4)
    
def AdjustPosition(turndata):
    dis1 = turndata[0]
    dis2 = turndata[1]
    turnAngle1 = turndata[2]
    turnAngle2 = turndata[3]

    motionPrx.setMoveArmsEnabled(False, False)
    motionPrx.moveTo(0.0,0.0,turnAngle1,moveConfig)
    motionPrx.setMoveArmsEnabled(False, False)
    motionPrx.moveTo(dis2,0.0,0.0,moveConfig)
    motionPrx.setMoveArmsEnabled(False, False)
    motionPrx.moveTo(0.0,0.0,turnAngle2,moveConfig)
    motionPrx.setMoveArmsEnabled(False, False)
    motionPrx.moveTo(0.0,dis1,0.0,moveConfig)  

def shougang():                       
    names = list()
    times = list()
    keys = list()

    names.append("HeadPitch")
    times.append([1, 2, 3, 4])
    keys.append([0, 0, 0, 0])

    names.append("HeadYaw")
    times.append([1, 2, 3, 4])
    keys.append([0, 0, 0, 0])

    names.append("LAnklePitch")
    times.append([1, 2, 3, 4])
    keys.append([-0.349794, -0.349794, -0.349794, -0.349794])

    names.append("LAnkleRoll")
    times.append([1, 2, 3, 4])
    keys.append([0, 0, 0, 0])

    names.append("LElbowRoll")
    times.append([1, 2, 3, 4])
    keys.append([-0.98632, -0.98632, -0.98632, -0.98632])

    names.append("LElbowYaw")
    times.append([1, 2, 3, 4])
    keys.append([-1.37757, -1.37757, -1.37757, -1.37757])

    names.append("LHand")
    times.append([1, 2, 3, 4])
    keys.append([0.2572, 0.2572, 0.2572, 0.2572])

    names.append("LHipPitch")
    times.append([1, 2, 3, 4])
    keys.append([-0.450955, -0.450955, -0.450955, -0.450955])

    names.append("LHipRoll")
    times.append([1, 2, 3, 4])
    keys.append([0, 0, 0, 0])

    names.append("LHipYawPitch")
    times.append([1, 2, 3, 4])
    keys.append([0, 0, 0, 0])

    names.append("LKneePitch")
    times.append([1, 2, 3, 4])
    keys.append([0.699462, 0.699462, 0.699462, 0.699462])

    names.append("LShoulderPitch")
    times.append([1, 2, 3, 4])
    keys.append([1.43885, 1.43885, 1.43885, 1.43885])

    names.append("LShoulderRoll")
    times.append([1, 2, 3, 4])
    keys.append([0.268407, 0.268407, 0.268407, 0.268407])

    names.append("LWristYaw")
    times.append([1, 2, 3, 4])
    keys.append([-0.016916, -0.016916, -0.016916, -0.016916])

    names.append("RAnklePitch")
    times.append([1, 2, 3, 4])
    keys.append([-0.354312, -0.354312, -0.354312, -0.354312])

    names.append("RAnkleRoll")
    times.append([1, 2, 3, 4])
    keys.append([0, 0, 0, 0])

    names.append("RElbowRoll")
    times.append([1, 2, 3, 4])
    keys.append([0.958791, 0.958791, 0.958791, 0.046062])

    names.append("RElbowYaw")
    times.append([1, 2, 3, 4])
    keys.append([1.67355, 1.67355, 1.21949, 1.19955])

    names.append("RHand")
    times.append([1, 2, 3, 4])
    keys.append([0.2216, 0.2216, 0.2216, 0.2216])

    names.append("RHipPitch")
    times.append([1, 2, 3, 4])
    keys.append([-0.451038, -0.451038, -0.451038, -0.451038])

    names.append("RHipRoll")
    times.append([1, 2, 3, 4])
    keys.append([0, 0, 0, 0])

    names.append("RHipYawPitch")
    times.append([1, 2, 3, 4])
    keys.append([0, 0, 0, 0])

    names.append("RKneePitch")
    times.append([1, 2, 3, 4])
    keys.append([0.699545, 0.699545, 0.699545, 0.699545])

    names.append("RShoulderPitch")
    times.append([1, 2, 3, 4, 5.2])
    keys.append([1.03856, 0.412688, 0.412688, 1.44967, 1.48528])

    names.append("RShoulderRoll")
    times.append([1, 2, 3, 4, 5.2])
    keys.append([0.265341, 0.294486, -0.285367, -0.963394, -0.349066])

    names.append("RWristYaw")
    times.append([1, 2, 3, 4])
    keys.append([-0.955723, -0.914306, -0.937315, 0.460158])
    motionPrx.setMoveArmsEnabled(False, False)
    motionPrx.angleInterpolation(names, keys, times, True)

def taishou():                        
    names = list()
    times = list()
    keys = list()

    names.append("HeadPitch")
    times.append([1.6, 2.84, 4.12])
    keys.append([0, 0, 0])

    names.append("HeadYaw")
    times.append([1.6, 2.84, 4.12])
    keys.append([0, 0, 0])

    names.append("LAnklePitch")
    times.append([1.6, 2.84, 4.12])
    keys.append([-0.349794, -0.349794, -0.349794])

    names.append("LAnkleRoll")
    times.append([1.6, 2.84, 4.12])
    keys.append([0, 0, 0])

    names.append("LElbowRoll")
    times.append([1.6, 2.84, 4.12])
    keys.append([-0.98632, -0.98632, -0.98632])

    names.append("LElbowYaw")
    times.append([1.6, 2.84, 4.12])
    keys.append([-1.37757, -1.37757, -1.37757])

    names.append("LHand")
    times.append([1.6, 2.84, 4.12])
    keys.append([0.2572, 0.2572, 0.2572])

    names.append("LHipPitch")
    times.append([1.6, 2.84, 4.12])
    keys.append([-0.450955, -0.450955, -0.450955])

    names.append("LHipRoll")
    times.append([1.6, 2.84, 4.12])
    keys.append([0, 0, 0])

    names.append("LHipYawPitch")
    times.append([1.6, 2.84, 4.12])
    keys.append([0, 0, 0])

    names.append("LKneePitch")
    times.append([1.6, 2.84, 4.12])
    keys.append([0.699462, 0.699462, 0.699462])

    names.append("LShoulderPitch")
    times.append([1.6, 2.84, 4.12])
    keys.append([1.43885, 1.43885, 1.43885])

    names.append("LShoulderRoll")
    times.append([1.6, 2.84, 4.12])
    keys.append([0.268407, 0.268407, 0.268407])

    names.append("LWristYaw")
    times.append([1.6, 2.84, 4.12])
    keys.append([-0.016916, -0.016916, -0.016916])

    names.append("RAnklePitch")
    times.append([1.6, 2.84, 4.12])
    keys.append([-0.354312, -0.354312, -0.354312])

    names.append("RAnkleRoll")
    times.append([1.6, 2.84, 4.12])
    keys.append([0, 0, 0])

    names.append("RElbowRoll")
    times.append([1.6, 2.84, 4.12])
    keys.append([0.046062, 0.958791, 0.958791])

    names.append("RElbowYaw")
    times.append([1.6, 2.84, 4.12])
    keys.append([1.19955, 1.21949, 1.67355])

    names.append("RHand")
    times.append([1.6, 2.84, 4.12])
    keys.append([0.2216, 0.2216, 0.2216])

    names.append("RHipPitch")
    times.append([1.6, 2.84, 4.12])
    keys.append([-0.451038, -0.451038, -0.451038])

    names.append("RHipRoll")
    times.append([1.6, 2.84, 4.12])
    keys.append([0, 0, 0])

    names.append("RHipYawPitch")
    times.append([1.6, 2.84, 4.12])
    keys.append([0, 0, 0])

    names.append("RKneePitch")
    times.append([1.6, 2.84, 4.12])
    keys.append([0.699545, 0.699545, 0.699545])

    names.append("RShoulderPitch")
    times.append([1.6, 2.84, 4.12])
    keys.append([1.44967, 0.412688, 0.412688])

    names.append("RShoulderRoll")
    times.append([1.6, 2.84, 4.12])
    keys.append([-0.963394, -0.285367, 0.294486])

    names.append("RWristYaw")
    times.append([1.6, 2.84, 4.12])
    keys.append([0.460158, -0.937315, -0.914306])
    motionPrx.setMoveArmsEnabled(False, False)
    motionPrx.angleInterpolation(names, keys, times, True)

def stop_and_losehand():
    
    while True:
        headif=memoryProxy.getData("RearTactilTouched")
        if headif==1.0:
            global stop1
            stop1=1
            print "Stop!!!!"
            tts.say("yes,i will stop !")
            motionPrx.openHand('RHand')   
            break

def TurnAfterHitball():
  
    motionPrx.angleInterpolationWithSpeed("HeadYaw", -0.0, 0.5)
   
    maxstepx = 0.04
    maxstepy = 0.14
    maxsteptheta = 0.4
    maxstepfrequency = 0.6
    stepheight = 0.02
    torsowx = 0.0
    torsowy = 0.0
    if (alpha < 0.0):
        motionPrx.setMoveArmsEnabled(False, False)
        motionPrx.moveTo(0.18,0.0,0.0,moveConfig)
        motionPrx.setMoveArmsEnabled(False, False)
        motionPrx.moveTo(0.0,0.0,-math.pi/2,moveConfig)
        motionPrx.setMoveArmsEnabled(False, False)
        motionPrx.moveTo(0.3,0.0,-math.pi*10/180,  moveConfig)              
    

    if (alpha > 0.0):
        motionPrx.setMoveArmsEnabled(False, False)
        motionPrx.moveTo(0.1,0.0,0.0,moveConfig)
        motionPrx.setMoveArmsEnabled(False, False)
        motionPrx.moveTo(0.0,0.0,math.pi/2,moveConfig)
        motionPrx.setMoveArmsEnabled(False, False)
        motionPrx.moveTo(0.3,0.0,0.0,moveConfig)
  

def firstSearchredball():
    currentCamera = "CameraBottom"
    camProxy.setActiveCamera(1)
    redballProxy.subscribe("redBallDetected")
    motionPrx.angleInterpolationWithSpeed("HeadYaw", 0.0, 0.5)
    motionPrx.angleInterpolationWithSpeed("HeadPitch", 0.0, 0.3)
    
    time.sleep(3.0)
    
    for i in range(0,3):
        ballDatatest = memoryProxy.getData("redBallDetected")
        
        if (ballDatatest==None):                             
            tts.say("where is red ball ?")  
            redballFlag = 1
            motionPrx.angleInterpolationWithSpeed("HeadYaw", 0.0, 0.5)
            motionPrx.setMoveArmsEnabled(False, False)
            
            allballDatatest = [[0],0,redballFlag]
            return allballDatatest
        else:
            wzCameratest = ballDatatest[1][0]
    print "0"
    print ballDatatest

    
    motionPrx.moveTo(0.03,0.0,0.0,moveConfig)    
    time.sleep(4.0)
    for i in range(0,3):
        
        ballData1 = memoryProxy.getData("redBallDetected")
        wzCamera1 = ballData1[1][0]
        wyCamera1 = ballData1[1][1]
        angularSize1 = ballData1[1][2]
        headangle1=motionPrx.getAngles("HeadYaw",True);
        
       
    print "1"
    print ballData1
    print "以上为前面数据"

   
    
    motionPrx.angleInterpolationWithSpeed("HeadYaw", 45*math.pi/180, 0.5)
    motionPrx.angleInterpolationWithSpeed("HeadPitch", 0.0, 0.3)
    time.sleep(4.0)
    for i in range(0,3):
        ballData2 = memoryProxy.getData("redBallDetected")
        wzCamera2 = ballData2[1][0]
        wyCamera2 = ballData2[1][1]
        angularSize2 = ballData2[1][2]
        headangle2=motionPrx.getAngles("HeadYaw",True);
    print "2"
    print ballData2
    print "以上为左边数据"
   

    motionPrx.angleInterpolationWithSpeed("HeadYaw", -45*math.pi/180, 0.5)
    motionPrx.angleInterpolationWithSpeed("HeadPitch", 0.0, 0.3)
    time.sleep(4.0)
    for i in range(0,3):
        ballData3 = memoryProxy.getData("redBallDetected")
        wzCamera3 = ballData3[1][0]
        wyCamera3 = ballData3[1][1]
        angularSize3 = ballData3[1][2]
        headangle3=motionPrx.getAngles("HeadYaw",True);
    print "3"
    print ballData3
    print "以上为右边数据"
    

    
    if (wzCamera1 != wzCameratest):
        tts.say("redball is in the front!")  
        redballFlag = 0                 
        allballData1 = [headangle1,ballData1,redballFlag]
        print allballData1
        return allballData1

    
    if (abs(wzCamera2 - wzCamera1)<=0.01 and abs(wzCamera3 - wzCamera2)<=0.01) and (wzCamera1 == wzCameratest):
        tts.say("where is red ball ?")  
        redballFlag = 1
        motionPrx.angleInterpolationWithSpeed("HeadYaw", 0.0, 0.5)
        motionPrx.setMoveArmsEnabled(False, False)
        
        allballDatatest = [[0],0,redballFlag]
        return allballDatatest

    
    if (abs(wzCamera2 - wzCamera1)>0.01 and abs(wzCamera3 - wzCamera2)<=0.01):
        tts.say("redball is in the left !")  
        redballFlag = 0
        allballData2 = [headangle2,ballData2,redballFlag]
        print allballData2
        return allballData2

    
    if (abs(wzCamera2 - wzCamera1)<=0.01 and abs(wzCamera3 - wzCamera2)>0.01):
        tts.say("redball is in the right !")  
        redballFlag = 0
        allballData3 = [headangle3,ballData3,redballFlag]
        print allballData3
        return allballData3

def CalculateRobotToRedball(allballData):
    h = 0.478
    
    headangle = allballData[0]       
    wzCamera = allballData[1][1][0]  
    wyCamera = allballData[1][1][1]  
    isenabled = False
    x = 0.0
    y = 0.0
    theta = headangle[0] + wzCamera

    motionPrx.setMoveArmsEnabled(False, False)
    
    motionPrx.angleInterpolationWithSpeed("HeadYaw", 0.0, 0.5)
    motionPrx.moveTo(x,y,theta,moveConfig) 
   
    time.sleep(3)                 
    val = memoryProxy.getData("redBallDetected")
    ballinfo = val[1]
    thetah = ballinfo[0]
    thetav = ballinfo[1]+(39.7*math.pi/180.0)
    x = h/(math.tan(thetav)) - 0.3  
    theta = thetah                 
    motionPrx.setMoveArmsEnabled(False, False)
    
    motionPrx.moveTo(0,0,theta,moveConfig)
    motionPrx.moveTo(x,y,0,moveConfig)     
        
    motionPrx.waitUntilMoveIsFinished()
    effectornamelist = ["HeadPitch"]
    timelist = [0.5]
    targetlist = [30*math.pi/180.0]
    motionPrx.angleInterpolation(effectornamelist,targetlist,timelist,isenabled)
    time.sleep(3)                         
    val = memoryProxy.getData("redBallDetected")
    ballinfo = val[1]
    thetah = ballinfo[0]
    thetav = ballinfo[1]+(69.7*math.pi/180.0)
    x = 0.0
    y = 0.0
    theta = thetah
    motionPrx.setMoveArmsEnabled(False, False)
    
    motionPrx.moveTo(x,y,theta,moveConfig)
    time.sleep(3)                 
    val = memoryProxy.getData("redBallDetected")
    ballinfo = val[1]
    thetah = ballinfo[0]
    thetav = ballinfo[1]+(69.7*math.pi/180.0)
    x = (h-0.1)/(math.tan(thetav)) - 0.05
    theta = thetah
    motionPrx.setMoveArmsEnabled(False, False)
    
    motionPrx.moveTo(x,y,theta,moveConfig)
    time.sleep(3)                
    
    val2=memoryProxy.getData("redBallDetected")
    ballinfo = val2[1]
    thetah = ballinfo[0]
    thetav = ballinfo[1]+(69.7*math.pi/180.0)
    dx = (h-0.1)/(math.tan(thetav))   
    return dx

def Precision():
    

    h = 0.478
    currentCamera = "CameraBottom"
    camProxy.setActiveCamera(1)
    redballProxy.subscribe("redBallDetected")
    motionPrx.angleInterpolationWithSpeed("HeadYaw", 0.0, 0.6)
    motionPrx.angleInterpolationWithSpeed("HeadPitch", 30*math.pi/180.0, 0.6)
    time.sleep(3)                                 
    val = memoryProxy.getData("redBallDetected")
    ballinfo = val[1]
    thetah = ballinfo[0]
    thetav = ballinfo[1]+(69.7*math.pi/180.0)
    x = (h-0.1)/(math.tan(thetav)) - 0.04        
    print x+0.04
    motionPrx.setMoveArmsEnabled(False, False)     
    motionPrx.moveTo(x,0,0,moveConfig)
    motionPrx.moveTo(0,-0.07,0,moveConfig)
    
    time.sleep(3)                                 
    val = memoryProxy.getData("redBallDetected")
    ballinfo = val[1]
    thetah = ballinfo[0]
    thetav = ballinfo[1]+(69.7*math.pi/180.0)
    x = (h-0.1)/(math.tan(thetav)) 
    print math.degrees(thetah)
    print math.degrees(ballinfo[1])
    print x
    redballProxy.unsubscribe("redBallDetected")


def firstSearchNAOmark():
    headYawAngle= -1.5
    camProxy.setActiveCamera(0)
    currentCamera = "CameraTop"

    motionPrx.angleInterpolationWithSpeed("HeadPitch", 0.0, 0.3)
    motionPrx.angleInterpolationWithSpeed("HeadYaw", 0.0, 0.3)
    landmarkProxy.subscribe("landmarkTest")
    markData = memoryProxy.getData("LandmarkDetected")
    while (headYawAngle < 1.5 ):
        motionPrx.angleInterpolationWithSpeed("HeadYaw", headYawAngle, 0.1)
        time.sleep(1)
        markData = memoryProxy.getData("LandmarkDetected")

        if(markData and isinstance(markData, list) and len(markData) >= 2):
            tts.say("i saw landmark!")
            landmarkFlag = 0   
           
            markwzCamera = markData[1][0][0][1]
            markwyCamera = markData[1][0][0][2]
            
            markangularSize = markData[1][0][0][3]
            print markwzCamera
            print markwyCamera
            print markangularSize
            headangle = motionPrx.getAngles("HeadYaw",True);
            print headangle                                
            markheadangle = markwzCamera + headangle[0]
            allmarkdata = [markwzCamera,markwyCamera,markangularSize,markheadangle,landmarkFlag]
            print allmarkdata
            return allmarkdata
            
            break
        else:
            tts.say("where is landmark ?")
            markwzCamera = 0
            markwyCamera = 0
            markangularSize = 0
        
        headYawAngle = headYawAngle + 0.5
    tts.say("i can not find landmark ! I will hit the ball directly ! ")
    print "landmark is not in sight !"
    landmarkFlag = 1    
    allmarkdata = [0,0,0,0,landmarkFlag]
    return allmarkdata
    landmarkProxy.unsubscribe("landmarkTest")

def robotTolandmark(allmarkdata):
    currentCamera = "CameraTop"
    landmarkTheoreticalSize = 0.10 
    wzCamera = allmarkdata[0]
    wyCamera = allmarkdata[1]
    angularSize = allmarkdata[2]
    angle = allmarkdata[3]   

    distanceFromCameraToLandmark = landmarkTheoreticalSize / ( 2 * math.tan( angularSize / 2))


    transform = motionPrx.getTransform(currentCamera, 2, True)
    transformList = almath.vectorFloat(transform)
    robotToCamera = almath.Transform(transformList)


    cameraToLandmarkRotationTransform = almath.Transform_from3DRotation(0, wyCamera, wzCamera)


    cameraToLandmarkTranslationTransform = almath.Transform(distanceFromCameraToLandmark, 0, 0)


    robotToLandmark = robotToCamera * cameraToLandmarkRotationTransform *cameraToLandmarkTranslationTransform
    x = robotToLandmark.r1_c4
    y = robotToLandmark.r2_c4
    z = robotToLandmark.r3_c4
    sdistance = math.sqrt(x*x+y*y)  
    robotTolandmarkdata = [angle,sdistance,x,y,z]
    print "x " + str(robotToLandmark.r1_c4) + " (in meters)"
    print "y " + str(robotToLandmark.r2_c4) + " (in meters)"
    print "z " + str(robotToLandmark.r3_c4) + " (in meters)"
    return robotTolandmarkdata

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
            dis1 = 0 - (x*math.sin(theta2) + 0.1)
            turnAngle2 = 0
            dis2 = x*math.cos(theta2)-0.09

        if theta < math.pi/2:
            theta2 = math.pi/2 - theta
            turnAngle1 = 0 - theta2
            dis1 = x*math.cos(theta) + 0.1             
            turnAngle2 = 0
            dis2 = x*math.sin(theta)-0.09

        
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
            dis1 = x*math.sin(theta2) + 0.1 
            turnAngle2 = 0
            dis2 = x*math.cos(theta2)-0.2


        if theta < math.pi/2:
            theta2 = math.pi/2 - theta
            turnAngle1 = theta2
            dis1 = -x*math.cos(theta)- 0.1
            turnAngle2 = 0
            dis2 = x*math.sin(theta)-0.2
        
        turndata = [dis1,dis2,turnAngle1,turnAngle2]
        return turndata  



def showNaoImage():
 
  resolution = 2    
  colorSpace = 11   
  camProxy.setActiveCamera(0)
  motionPrx.angleInterpolationWithSpeed("HeadYaw", 0.0, 0.5)
  motionPrx.angleInterpolationWithSpeed("HeadPitch", 15*math.pi/180, 0.3)
  videoClient = camProxy.subscribe("python_client", resolution, colorSpace, 5)
  time.sleep(2)
  t0 = time.time()
  
  naoImage = camProxy.getImageRemote(videoClient)

  t1 = time.time()


  print "acquisition delay ", t1 - t0
 
  camProxy.unsubscribe(videoClient)
  

  
  imageWidth = naoImage[0]
  imageHeight = naoImage[1]
  array = naoImage[6]

 
  img = Image.frombytes("RGB", (imageWidth, imageHeight), array)


 
  img.save("camImage.png", "PNG")


def Analyize():
  img = cv2.imread("camImage.png", cv2.IMREAD_UNCHANGED)
  

  img=img[100:,:,:]  
  channelB = img[:,:,0]
  channelG = img[:,:,1]
  channelR = img[:,:,2]

 
  Hm = 6
  channelB = channelB*0.1*Hm
  channelG = channelG*0.1*Hm
  channelR = channelR - channelB - channelG
  channelR = 3*channelR
  channelR = cv2.GaussianBlur(channelR, (9,9), 1.5)
  channelR[channelR<0] = 0
  channelR[channelR>255] = 255


  image=np.uint8(np.round(channelR))
  print(type(image))
  print(image.shape)   

 

  circles = cv2.HoughCircles(image, cv2.HOUGH_GRADIENT, dp=1, minDist=400, param1=150, param2=10, minRadius=3, maxRadius=25)
  theta=0
  if circles is None:
    return 0
  else:
    print(len(circles))
    circle = circles[0,:,:] 
    print(circle)   
    y=circle[0][0]
    degree=(320-y)/640*60.97
    print degree
    theta=degree*math.pi/180


    circles = np.uint16(np.around(circles))
    for i in circles[0,:]:
       
        cv2.circle(img,(i[0],i[1]),i[2],(0,255,0),2)  
        
        cv2.circle(img,(i[0],i[1]),2,(0,0,255),3)

   
    return theta
 

AutoProxy.setState("disabled")
motionPrx.stiffnessInterpolation("Body", 1 , 1)
postureProxy.goToPosture("StandInit", 1.0)

alpha = -math.pi/2



zhuagan()  
headtouch()  
time.sleep(1)

motionPrx.angleInterpolationWithSpeed(PositionJointNamesR,golfPositionJointAnglesR1,0.4)
motionPrx.angleInterpolationWithSpeed(PositionJointNamesR,golfPositionJointAnglesR2,0.4)
motionPrx.angleInterpolationWithSpeed(PositionJointNamesR,golfPositionJointAnglesR3,0.4)
time.sleep(3)
motionPrx.angleInterpolationWithSpeed(PositionJointNamesR,golfPositionJointAnglesR4,0.08)       
time.sleep(2)
motionPrx.angleInterpolationWithSpeed(PositionJointNamesR,golfPositionJointAnglesR1,0.4)

shougang()  
TurnAfterHitball()


motionPrx.moveTo(0.3,0.0,0,moveConfig)
for i in range(2):
    showNaoImage()
    theta=Analyize()
    motionPrx.moveTo(0,0.0,theta,moveConfig)
    motionPrx.moveTo(0.3,0.0,0,moveConfig)
    motionPrx.waitUntilMoveIsFinished()
allballData = firstSearchredball()   
print type(allballData[1])
while (type(allballData[1])!=list):
    showNaoImage()
    theta=Analyize()
    motionPrx.moveTo(0,0.0,theta,moveConfig)
    motionPrx.moveTo(0.15,0.0,0,moveConfig)
    allballData = firstSearchredball() 
x = CalculateRobotToRedball(allballData)
print   x
taishou()
HitBall()                              
shougang()
TurnAfterHitball()                      






motionPrx.moveTo(0.5,0.0,-math.pi*10/180,moveConfig) 
motionPrx.moveTo(0.5,0.0,0,moveConfig) 
showNaoImage()
Analyize()
for  i in range(3):
    showNaoImage()
    theta=Analyize()
    motionPrx.moveTo(0,0.0,theta,moveConfig)
    motionPrx.moveTo(0.4,0.0,0,moveConfig)
allballData = firstSearchredball()   
print type(allballData[1])
while (type(allballData[1])!=list):
    showNaoImage()
    theta=Analyize()
    motionPrx.moveTo(0,0.0,theta,moveConfig)
    motionPrx.moveTo(0.3,0.0,0,moveConfig)
    allballData = firstSearchredball()         
x = CalculateRobotToRedball(allballData)                   
print   x




allmarkdata = firstSearchNAOmark()  
robotTolandmarkdata = robotTolandmark(allmarkdata)
s = robotTolandmarkdata[1]            
alpha = robotTolandmarkdata[0]      
turndata = TriangleCalculation(x,s,alpha)  
 
turndata[1]+=-0.05                                          
AdjustPosition(turndata)                
Precision()
taishou()
motionPrx.angleInterpolationWithSpeed(PositionJointNamesR,golfPositionJointAnglesR1,0.4)
motionPrx.angleInterpolationWithSpeed(PositionJointNamesR,golfPositionJointAnglesR2,0.4)
motionPrx.angleInterpolationWithSpeed(PositionJointNamesR,golfPositionJointAnglesR3,0.4)
time.sleep(3)
motionPrx.angleInterpolationWithSpeed(PositionJointNamesR,golfPositionJointAnglesR4,0.05)
time.sleep(2)
motionPrx.angleInterpolationWithSpeed(PositionJointNamesR,golfPositionJointAnglesR1,0.4)
shougang()




