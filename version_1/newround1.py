from naoqi import ALProxy
import sys
sys.path.append(r'/home/nao/pynaoqi')
import almath
import time
import math
import motion
import thread
from PIL import Image

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
moveConfig1 = [["MaxStepX",0.02],
            ["MaxStepY",0.1],
            ["MaxStepTheta",maxsteptheta],
            ["MaxStepFrequency",maxstepfrequency],
            ["StepHeight",stepheight],
            ["TorsoWx",torsowx],
            ["TorsoWy",torsowy]]


def openHand():

    startplayBall()

    name = 'RHand'
    angleLists=[0.57,0.10]
    timeList = [1.0,6.0]
    isAbsolute=True
    motionPrx.angleInterpolation(name,angleLists,timeList,isAbsolute)
    motionPrx.waitUntilMoveIsFinished()

def defPosture():
   
    names = ['RShoulderPitch',
             'RShoulderRoll',
             'RElbowRoll',
             'RElbowYaw',
             'RWristYaw']
    angleLists=[84.6*almath.TO_RAD,
               -18.2*almath.TO_RAD,
               2.5*almath.TO_RAD,
               88.9*almath.TO_RAD,
               -11.3*almath.TO_RAD]
    maxSpeedFraction=0.2
    motionPrx.angleInterpolationWithSpeed(names,angleLists,maxSpeedFraction)
    motionPrx.waitUntilMoveIsFinished()

def endPlay():
    
    names = ['RShoulderPitch',
             'RShoulderRoll',
             'RElbowRoll',
             'RElbowYaw',
             'RWristYaw']
    angleLists=[[-3.0*almath.TO_RAD,15.2*almath.TO_RAD],
                [15.6*almath.TO_RAD,-38.6*almath.TO_RAD],
                [27.0*almath.TO_RAD,20.7*almath.TO_RAD],
                [95.4*almath.TO_RAD,90.1*almath.TO_RAD],
                [-17.1*almath.TO_RAD,4.9*almath.TO_RAD]]
    timeList = [[1.0,3.0],
                [1.0,2.0],
                [1.0,3.0],
                [1.0,3.0],
                [1.0,2.0]]
    isAbsolute=True
    motionPrx.angleInterpolation(names,angleLists,timeList,isAbsolute)

    defPosture()

def startplayBall():
    
    names = ['RShoulderPitch',
             'RShoulderRoll',
             'RElbowRoll',
             'RElbowYaw',
             'RWristYaw']
    angleLists=[[15.2*almath.TO_RAD,-3.0*almath.TO_RAD],
                [-38.6*almath.TO_RAD,15.6*almath.TO_RAD],
                [20.7*almath.TO_RAD,27.0*almath.TO_RAD],
                [90.1*almath.TO_RAD,95.4*almath.TO_RAD],
                [4.9*almath.TO_RAD,-17.1*almath.TO_RAD]]
    timeList = [[1.0,3.0],
                [1.0,2.0],
                [1.0,3.0],
                [1.0,3.0],
                [1.0,2.0]]
    isAbsolute=True
    motionPrx.angleInterpolation(names,angleLists,timeList,isAbsolute)
    time.sleep(1.0)


    names = ['RShoulderPitch',
             'RShoulderRoll',
             'RElbowRoll',
             'RElbowYaw',
             'RWristYaw']
    angleLists=[47.8*almath.TO_RAD,
               15.6*almath.TO_RAD,
               40.0*almath.TO_RAD,
               99.1*almath.TO_RAD,
               9.8*almath.TO_RAD]
    maxSpeedFraction=0.2
    motionPrx.angleInterpolationWithSpeed(names,angleLists,maxSpeedFraction)

def playBall():
    
    name = 'RWristYaw'
    angleLists = [23.3*almath.TO_RAD,-73.6*almath.TO_RAD]
    timeList=[1.0,1.5]
    isAbsolute=True
    motionPrx.angleInterpolation(name,angleLists,timeList,isAbsolute)

def zhuagan():
    while True:
        RighthandTouchedFlag = memoryProxy.getData("HandRightRightTouched")
        if RighthandTouchedFlag == 1.0:
            print "right hand touched"
            tts.say("give me a club ")
            openHand()
            break

def headtouch():
    while True:
        headTouchedButtonFlag = memoryProxy.getData("FrontTactilTouched")
        if headTouchedButtonFlag == 1.0:
            print "front head touched"
            tts.say("begin the round three")
            break

def HitBall():
    playBall()
    
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
   
    time.sleep(1.5)
    val = memoryProxy.getData("redBallDetected")
    ballinfo = val[1]
    thetah = ballinfo[0]
    thetav = ballinfo[1]+(39.7*math.pi/180.0)
    x = h/(math.tan(thetav)) - 0.3
    theta = 0.0
    motionPrx.setMoveArmsEnabled(False, False)
    
    motionPrx.moveTo(x,y,theta,moveConfig)
        
    motionPrx.waitUntilMoveIsFinished()
    effectornamelist = ["HeadPitch"]
    timelist = [0.5]
    targetlist = [30*math.pi/180.0]
    motionPrx.angleInterpolation(effectornamelist,targetlist,timelist,isenabled)
    time.sleep(1.5)
    val = memoryProxy.getData("redBallDetected")
    ballinfo = val[1]
    thetah = ballinfo[0]
    thetav = ballinfo[1]+(69.7*math.pi/180.0)
    x = 0.0
    y = 0.0
    theta = thetah
    motionPrx.setMoveArmsEnabled(False, False)
    
    motionPrx.moveTo(x,y,theta,moveConfig)
    
    time.sleep(1.5)
    val = memoryProxy.getData("redBallDetected")
    ballinfo = val[1]
    thetah = ballinfo[0]
    thetav = ballinfo[1]+(69.7*math.pi/180.0)
    x = (h-0.1)/(math.tan(thetav)) - 0.07
    theta = thetah
    motionPrx.setMoveArmsEnabled(False, False)
    
    motionPrx.moveTo(x,y,theta,moveConfig)
    
    time.sleep(1.5)
      
    val2=memoryProxy.getData("redBallDetected")
    ballinfo = val2[1]
    thetah = ballinfo[0]
    thetav = ballinfo[1]+(69.7*math.pi/180.0)
    dx = (h-0.1)/(math.tan(thetav))   
    return dx
def AdjustPosition(turndata):
    dis1 = turndata[0]
    dis2 = turndata[1]
    turnAngle1 = turndata[2]
    turnAngle2 = turndata[3]

    motionPrx.setMoveArmsEnabled(False, False)
    motionPrx.moveTo(0.0,0.0,turnAngle1,moveConfig1)
    motionPrx.setMoveArmsEnabled(False, False)
    motionPrx.moveTo(dis2,0.0,0.0,moveConfig)
    motionPrx.setMoveArmsEnabled(False, False)
    motionPrx.moveTo(0.0,0.0,turnAngle2,moveConfig1)
    motionPrx.setMoveArmsEnabled(False, False)
    motionPrx.moveTo(0.0,dis1,0.0,moveConfig)  

def shougang():                      
    endPlay()
    motionPrx.setMoveArmsEnabled(False, False)

def taishou():                        
    startplayBall()
    
def firstSearchredball():
    currentCamera = "CameraBottom"
    camProxy.setActiveCamera(1)
    redballProxy.subscribe("redBallDetected")
    motionPrx.angleInterpolationWithSpeed("HeadYaw", 0.0, 0.5)
    motionPrx.angleInterpolationWithSpeed("HeadPitch", 0.0, 0.3)
    
    time.sleep(3.0)
    
    for i in range(0,3):
        ballDatatest = memoryProxy.getData("redBallDetected")
        if(ballDatatest and isinstance(ballDatatest, list) and len(ballDatatest) >= 2):
            ballDatatest = memoryProxy.getData("redBallDetected")
            wzCameratest = ballDatatest[1][0]
    

    
    motionPrx.moveTo(0.03,0.0,0.0)    
    time.sleep(4.0)
    for i in range(0,3):
        ballData1 = memoryProxy.getData("redBallDetected")
        if(ballData1 and isinstance(ballData1, list) and len(ballData1) >= 2):
            ballData1 = memoryProxy.getData("redBallDetected")
            wzCamera1 = ballData1[1][0]
            wyCamera1 = ballData1[1][1]
            angularSize1 = ballData1[1][2]
            headangle1=motionPrx.getAngles("HeadYaw",True);
        else:
            tts.say("redball is not in the front !")
    print "1"
    print ballData1

    
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
        motionPrx.moveTo(0.4,0.0,0.0,moveConfig)   
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




motionPrx.stiffnessInterpolation("Body", 1 , 1)
postureProxy.goToPosture("StandInit", 1.0)
AutoProxy.setState("safeguard")
thread.start_new(stop_and_losehand,())


zhuagan()  
headtouch()  
time.sleep(1)

shougang()  


allballData = firstSearchredball()   
x = CalculateRobotToRedball(allballData)
print   x
turndata=[-0.20,-0.07,math.pi*90/180,0]     
AdjustPosition(turndata)                
taishou()
HitBall()                              
time.sleep(1.0)
shougang()
        



