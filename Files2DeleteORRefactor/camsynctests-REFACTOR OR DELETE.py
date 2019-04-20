#!/usr/bin/env python
# Software License Agreement (BSD License)
import numpy as np
import cv2
import pickler as pickle
import datetime
import aruco
import open3d


## Simple talker demo that listens to std_msgs/Strings published 
## to the 'chatter' topic

import rospy
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import CameraInfo
from sensor_msgs.msg import Image
import rosinterface as roscv
import visu
import procrustes as proc
import time

class InfoGetter(object):
    def __init__(self):
      
        self.count = 0
        self.c1=np.random.rand(480,640,3)
        self.c2=np.random.rand(480,640,3)
        self.active1=False
        self.active2=False

        self.interval = 1

    def showIms(self):

        cv2.imshow("yomamma",self.c1)

        cv2.imshow("yomamma2",self.c2)

        cv2.waitKey(3)

        

    def callback1(self,data):


        img = roscv.rosImg2RGB(data)


        self.c1=img
        self.showIms()
        
        #rospy.sleep(self.interval)
        

    def callback2(self,data):
        
        img = roscv.rosImg2RGB(data)


        self.c2=img
        #self.showIms()
        

        #rospy.sleep(self.interval)
        







ig = InfoGetter()

cameraNames = ["abretesesamo","ervilhamigalhas"]
rospy.init_node('my_name_is_jeff', anonymous=True)

#subscribe


rospy.Subscriber(cameraNames[0]+"/rgb/image_color", Image, ig.callback1)

rospy.Subscriber(cameraNames[1]+"/rgb/image_color", Image, ig.callback2)


try:
    rospy.spin()
except KeyboardInterrupt:
    print("shut")


cv2.imshow("im1",ig.c1)
cv2.imshow("im2",ig.c2)
cv2.waitKey(0)


print "ola"