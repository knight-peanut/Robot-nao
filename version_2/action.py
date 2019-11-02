# -*- coding: cp936 -*-

import sys
sys.path.append(r'/home/nao/pynaoqi')
from configureNao import ConfigureNao
from naoqi import ALProxy
import math
import almath
import time

class MotionBasis(ConfigureNao):
        def __init__(self,IP,PORT=9559):
                super(MotionBasis,self).__init__(IP,PORT)
                #右手关节参数 [右肩关节前后动，右肩关节左右动，右肘关节，右肩关节扭动，右腕关节扭转，右手打开/合拢]
                self.PositionJointNamesR  = ["RShoulderPitch", "RShoulderRoll", "RElbowYaw", "RElbowRoll", "RWristYaw","RHand"]
                self.golfPositionJointAnglesR1  = [1.01402, 0.314159, 1.62907, 1.48035, -0.648924,  0.12]
                self.golfPositionJointAnglesR2  = [1.02629, 0.314159, 1.62907, 1.48342, 0.230058, 0.12]
                self.golfPositionJointAnglesR3  = [1.03549, 0.314159, 1.64747, 0.998676, 0.476658,  0.12]
                self.golfPositionJointAnglesR4  = [1.03549, 0.314159, 1.66742, 0.971064, -0.980268, 0.12]
                self.golfPositionJointAnglesR5  = [1.07998, 0.314159, 1.61986, 1.11679, 0.082794, 0.6]  
                self.golfPositionJointAnglesR6  = [1.07998, 0.314159, 1.61986, 1.11679, 0.082794, 0.12]  
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
        def zhuagan(self):
                 while True:
                        RighthandTouchedFlag = self.memoryProxy.getData("HandRightRightTouched")#HandRightRightTouched对应的动作为触摸右手右触觉传感器（人为）时抬起
                        if RighthandTouchedFlag == 1.0:
                                print "right hand touched"#如果触摸右手右触觉传感器，则为1.0
                                self.tts.say("give me a club ")
                                self.motionProxy.angleInterpolationWithSpeed(self.PositionJointNamesR,self.golfPositionJointAnglesR5,0.4);
                                time.sleep(10)
                                self.motionProxy.angleInterpolationWithSpeed(self.PositionJointNamesR,self.golfPositionJointAnglesR6,0.4);
                                
                                time.sleep(1)
                                self.motionProxy.angleInterpolationWithSpeed(self.PositionJointNamesR,self.golfPositionJointAnglesR2,0.4)
                                self.motionProxy.angleInterpolationWithSpeed(self.PositionJointNamesR,self.golfPositionJointAnglesR3,0.4)
                                time.sleep(3)
                                self.motionProxy.angleInterpolationWithSpeed(self.PositionJointNamesR,self.golfPositionJointAnglesR4,0.12)
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
                
                if (self.alpha<0):
                        self.motionProxy.angleInterpolationWithSpeed(self.PositionJointNamesR,self.golfPositionJointAnglesR1,0.4)
                        self.motionProxy.angleInterpolationWithSpeed(self.PositionJointNamesR,self.golfPositionJointAnglesR2,0.4)
                        self.motionProxy.angleInterpolationWithSpeed(self.PositionJointNamesR,self.golfPositionJointAnglesR3,0.4)
                        time.sleep(3)
                        self.motionProxy.angleInterpolationWithSpeed(self.PositionJointNamesR,self.golfPositionJointAnglesR4,hitballSpeed)
                        time.sleep(2)
                        self.motionProxy.angleInterpolationWithSpeed(self.PositionJointNamesR,self.golfPositionJointAnglesR1,0.8)
                if (self.alpha>0):
                        self.motionProxy.angleInterpolationWithSpeed(self.PositionJointNamesR,self.golfPositionJointAnglesR2,0.4)
                        self.motionProxy.angleInterpolationWithSpeed(self.PositionJointNamesR,self.golfPositionJointAnglesR1,0.4)
                        self.motionProxy.angleInterpolationWithSpeed(self.PositionJointNamesR,self.golfPositionJointAnglesR4,0.4)
                        time.sleep(3)
                        self.motionProxy.angleInterpolationWithSpeed(self.PositionJointNamesR,self.golfPositionJointAnglesR3,0.12)
                        time.sleep(2)
                        self.motionProxy.angleInterpolationWithSpeed(self.PositionJointNamesR,self.golfPositionJointAnglesR1,0.8)
            
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

        #step4
        def shougan(self):                       
                names = list()
                times = list()
                keys = list()

                names.append("HeadPitch")#头部关节前后动
                times.append([1, 2, 3, 4])
                keys.append([0, 0, 0, 0])

                names.append("HeadYaw")#头部关节扭动
                times.append([1, 2, 3, 4])
                keys.append([0, 0, 0, 0])

                names.append("LAnklePitch")#左踝关节前后动（-70.5至54）
                times.append([1, 2, 3, 4])
                keys.append([-0.349794, -0.349794, -0.349794, -0.349794])

                names.append("LAnkleRoll")#左踝关节前后动（45至25）
                times.append([1, 2, 3, 4])
                keys.append([0, 0, 0, 0])

                names.append("LElbowRoll")#左肩关节扭转
                times.append([1, 2, 3, 4])
                keys.append([-0.98632, -0.98632, -0.98632, -0.98632])

                names.append("LElbowYaw")#左肘关节
                times.append([1, 2, 3, 4])
                keys.append([-1.37757, -1.37757, -1.37757, -1.37757])

                names.append("LHand")#左手
                times.append([1, 2, 3, 4])
                keys.append([0.2572, 0.2572, 0.2572, 0.2572])

                names.append("LHipPitch")#左髋关节左右动（-104.5至28.5）
                times.append([1, 2, 3, 4])
                keys.append([-0.450955, -0.450955, -0.450955, -0.450955])

                names.append("LHipRoll")#左髋关节左右动
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
                #left and right
                self.motionProxy.setMoveArmsEnabled(False, False)
                #将一个或多个关节插值到目标角度或沿着定时轨迹。True表示以绝对角度描述运动
                self.motionProxy.angleInterpolation(names, keys, times, True)

        #step5
        def taishou(self):                        
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
                #left and right
                self.motionProxy.setMoveArmsEnabled(False, False)
                #isAbsolute - 如果为true，则以绝对角度描述运动，否则角度相对于当前角度
                self.motionProxy.angleInterpolation(names, keys, times, True)


        def setalpha(self,alpha):
                self.alpha=alpha
        
