from naoqi import ALProxy
import sys
import numpy as np
sys.path.append(r'/home/nao/pynaoqi')
import almath
import time
import math
import motion
import thread
import cv2
from PIL import Image


PORT=9559               
robotIP="127.0.0.1"   

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


#---------------------------------------------initialize object----------------------------------------------#
memoryProxy = ALProxy("ALMemory", robotIP ,PORT)        #  memory  object
motionPrx = ALProxy("ALMotion", robotIP , PORT)      #  motion  object
tts = ALProxy("ALTextToSpeech", robotIP, PORT)
postureProxy = ALProxy("ALRobotPosture", robotIP , PORT)
memoryProxy = ALProxy("ALMemory", robotIP , PORT)
redballProxy = ALProxy("ALRedBallDetection", robotIP , PORT)
camProxy = ALProxy("ALVideoDevice", robotIP, PORT)
landmarkProxy = ALProxy("ALLandMarkDetection", robotIP, PORT)
AutoProxy=ALProxy("ALAutonomousLife",robotIP,PORT)




def showNaoImage():#
  """
  First get an image from Nao, then show it on the screen with PIL.
  """
  resolution = 2    # VGA
  colorSpace = 11   # RGB
  camProxy.setActiveCamera(0)
  motionPrx.angleInterpolationWithSpeed("HeadYaw", 0.0, 0.5)
  motionPrx.angleInterpolationWithSpeed("HeadPitch", 15*math.pi/180, 0.3)
  videoClient = camProxy.subscribe("python_client", resolution, colorSpace, 5)
  time.sleep(2)
  t0 = time.time()
  # Get a camera image.
  # image[6] contains the image data passed as an array of ASCII chars.
  naoImage = camProxy.getImageLoacl(videoClient)

  t1 = time.time()

  # Time the image transfer.
  print "acquisition delay ", t1 - t0
 
  camProxy.unsubscribe(videoClient)
  # Now we work with the image returned and save it as a PNG  using ImageDraw
  # package.

  # Get the image size and pixel array.
  imageWidth = naoImage[0]
  imageHeight = naoImage[1]
  array = naoImage[6]

  # Create a PIL Image from our pixel array.
  #img = Image.fromstring("RGB", (imageWidth, imageHeight), array)
  img = Image.frombytes("RGB", (imageWidth, imageHeight), array)


  # Save the image.
  img.save("camImage.png", "PNG")
  #return img

def Analyize():
  img = cv2.imread("camImage.png", cv2.IMREAD_UNCHANGED)
  #print(img.shape)   
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
  print(image.shape)   #480*640
  #cv2.imshow("gray", image)

  circles = cv2.HoughCircles(image, cv2.HOUGH_GRADIENT, dp=1, minDist=400, param1=150, param2=10, minRadius=3, maxRadius=25)
  theta=0
  if circles is None:
    return 0
    tts.say("i dont know the direction of the red ball")
  else:
    print(len(circles))
    circle = circles[0,:,:] 
    print(circle)   
    y=circle[0][0]
    degree=(320-y)/640*60.97
    print degree
    theta=degree*math.pi/180

  return theta
 
AutoProxy.setState("safeguard")
postureProxy.goToPosture("StandInit", 1.0)
showNaoImage()
theta=Analyize()
motionPrx.moveTo(0,0.0,theta,moveConfig)
motionPrx.moveTo(0.3,0.0,0,moveConfig)
