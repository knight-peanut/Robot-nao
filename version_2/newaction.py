# -*- coding: cp936 -*-

import sys
sys.path.append(r'/home/nao/pynaoqi')
from configureNao import ConfigureNao
from naoqi import ALProxy
import math
import almath
import time

class NewMotionBasis(ConfigureNao):
        def __init__(self,IP,PORT=9559):
                super(NewMotionBasis,self).__init__(IP,PORT)
                
                self.names = ['RShoulderPitch','RShoulderRoll','RElbowRoll','RWristYaw','RElbowYaw']
                
                self.alpha=-math.pi/2
                
                self.maxstepx = 0.04
                self.maxstepy = 0.14
                self.maxsteptheta = 0.4
                self.maxstepfrequency = 0.6
                self.stepheight = 0.02
                self.torsowx = 0.0
                self.torsowy = 0.0
                self.moveConfig = [["MaxStepX",self.maxstepx],
                                    ["MaxStepY",self.maxstepy],
                                    ["MaxStepTheta",self.maxsteptheta],
                                    ["MaxStepFrequency",self.maxstepfrequency],
                                    ["StepHeight",self.stepheight],
                                    ["TorsoWx",self.torsowx],
                                    ["TorsoWy",self.torsowy]]


        

        #step1
        def GrabRod(self):
                 while True:
                        RighthandTouchedFlag = self.memoryProxy.getData("HandRightRightTouched")#HandRightRightTouched对应的动作为触摸右手右触觉传感器（人为）时抬起
                        if RighthandTouchedFlag == 1.0:
                                print "right hand touched"#如果触摸右手右触觉传感器，则为1.0
                                self.tts.say("give me a club ")
                                targetAngle = [67.7*almath.TO_RAD,3.2*almath.TO_RAD,73.8*almath.TO_RAD,6.2*almath.TO_RAD,93.7*almath.TO_RAD]
                                maxSpeedFraction = 0.2
                                self.motionProxy.angleInterpolationWithSpeed(self.names,targetAngle,maxSpeedFraction)

                                time.sleep(2.0)

                                name = 'RHand'
                                targetAngle = 0.68
                                self.motionProxy.angleInterpolationWithSpeed(name,targetAngle,maxSpeedFraction)

                                time.sleep(5.0)

                                targetAngle = 0.14
                                self.motionProxy.angleInterpolationWithSpeed(name,targetAngle,maxSpeedFraction)

                                time.sleep(2.0)

                                break

        #step2
        def headtouch(self):
                while True:
                        headTouchedButtonFlag = self.memoryProxy.getData("FrontTactilTouched")#FrontTactilTouched对应动作触摸前头tactil传感器时（由人类触摸）引发
                        if headTouchedButtonFlag == 1.0:
                                print "front head touched"#如果触摸前头tactil传感器，则为1.0
                                self.tts.say("begin the round three")
                                break

        #step3
        def HitBall(self,hitballSpeed):
                
                targetList = [[94.0*almath.TO_RAD,41.3*almath.TO_RAD],
                              [-13.0*almath.TO_RAD,-36.5*almath.TO_RAD,2.8*almath.TO_RAD],
                              [19.3*almath.TO_RAD,72.8*almath.TO_RAD],
                              [8.4*almath.TO_RAD,-3.5*almath.TO_RAD,6.3*almath.TO_RAD],
                              [88.5*almath.TO_RAD,73.7*almath.TO_RAD,94.1*almath.TO_RAD]]

                timeList = [[1.0,3.0],
                            [1.0,2.0,4.0],
                            [1.0,3.0],
                            [1.0,2.0,4.0],
                            [1.0,2.0,3.0]]

                isAbsolute = True

                self.motionProxy.angleInterpolation(self.names,targetList,timeList,isAbsolute)

                time.sleep(1.0)

                if(self.alpha<0):
                    #决定打球方向
                    targetAngle = [67.7*almath.TO_RAD,3.2*almath.TO_RAD,73.8*almath.TO_RAD,48.8*almath.TO_RAD,93.7*almath.TO_RAD]
                    maxSpeedFraction = 0.2
                    self.motionProxy.angleInterpolationWithSpeed(self.names,targetAngle,maxSpeedFraction)

                    time.sleep(3.0)

                    #打球
                    name = 'RWristYaw'
                    targetAngle = -39.1*almath.TO_RAD
                    self.motionProxy.angleInterpolationWithSpeed(name,targetAngle,hitballSpeed)

                if(self.alpha>0):

                    
                    targetAngle = [67.7*almath.TO_RAD,3.2*almath.TO_RAD,73.8*almath.TO_RAD,-37.7*almath.TO_RAD,93.7*almath.TO_RAD]
                    maxSpeedFraction = 0.2
                    self.motionProxy.angleInterpolationWithSpeed(self.names,targetAngle,maxSpeedFraction)

                    time.sleep(3.0)

                    #打球
                    name = 'RWristYaw'
                    targetAngle = 34.7*almath.TO_RAD
                    self.motionProxy.angleInterpolationWithSpeed(name,targetAngle,hitballSpeed)
                    
            
        def AdjustPosition(self,turndata):
                dis1 = turndata[0]
                dis2 = turndata[1]
                turnAngle1 = turndata[2]
                turnAngle2 = turndata[3]

                self.motionProxy.setMoveArmsEnabled(False, False)
                self.motionProxy.moveTo(0.0,0.0,turnAngle1,self.moveConfig)
                self.motionProxy.setMoveArmsEnabled(False, False)
                self.motionProxy.moveTo(dis2,0.0,0.0,self.moveConfig)
                self.motionProxy.setMoveArmsEnabled(False, False)
                self.motionProxy.moveTo(0.0,0.0,turnAngle2,self.moveConfig)
                self.motionProxy.setMoveArmsEnabled(False, False)
                self.motionProxy.moveTo(0.0,dis1,0.0,self.moveConfig)  


        def setalpha(self,alpha):
                self.alpha=alpha



        def CloseRod(self):
    
                targetList = [[41.3*almath.TO_RAD,94.0*almath.TO_RAD],
                              [2.8*almath.TO_RAD,-36.5*almath.TO_RAD,-13.0*almath.TO_RAD],
                              [72.8*almath.TO_RAD,19.3*almath.TO_RAD],
                              [6.3*almath.TO_RAD,-3.5*almath.TO_RAD,8.4*almath.TO_RAD],
                              [94.1*almath.TO_RAD,73.7*almath.TO_RAD,88.5*almath.TO_RAD]]


                timeList = [[1.0,3.0],
                            [1.0,2.0,4.0],
                            [1.0,3.0],
                            [1.0,2.0,4.0],
                            [1.0,2.0,3.0]]

                isAbsolute = True

                self.motionProxy.angleInterpolation(self.names,targetList,timeList,isAbsolute)

                time.sleep(2.0)

        def LoseHand(self):
                while True:
                        headFlag=self.memoryProxy.getData("RearTactilTouched")
                        if headFlag==1.0:                    
                            self.tts.say("i will stop !")
                            self.motionProxy.openHand('RHand')   
                            break


        
