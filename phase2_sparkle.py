#!/usr/bin/env python
# Software License Agreement (BSD License)
import numpy as np
import cv2

import pickler as pickle

import datetime

import aruco

import Tkinter as tkinter
import PIL.Image, PIL.ImageTk

import matplotlib
from matplotlib import pyplot as plt
matplotlib.use('Agg')
## Simple talker demo that listens to std_msgs/Strings published 
## to the 'chatter' topic

import rospy

from sensor_msgs.msg import CameraInfo
from sensor_msgs.msg import Image
import rosinterface as roscv
import visu

import time

def callback(data,args):

    K=args[0]
    D=args[1]

    print(time.time())
    #rospy.loginfo(rospy.get_caller_id() + 'I heard it')
    imagem = roscv.rosImg2RGB(data)
    
    det_corners, ids, rejected = aruco.FindMarkers(imagem, K)

    hello = imagem.astype(np.uint8).copy() 
    hello = cv2.aruco.drawDetectedMarkers(hello,det_corners,ids)

    rots,tvecs,img = aruco.FindPoses(K,D,det_corners,hello,len(ids))

    print(img)
    print("hi")
    #cv2.imshow("wow",img)

    #time.sleep(10)
    

    

def main():

    datdata={}

    cameraName = "camera"
    rgb=0

    rospy.init_node('my_name_is_jeff', anonymous=True)
    camInfo = rospy.wait_for_message("/camera/rgb/camera_info", CameraInfo)
        
    #rgb,depth = roscv.GetRGBD(cameraName)
    
    K = np.asarray(camInfo.K).reshape((3,3))

    #det_corners, ids, rejected = aruco.FindMarkers(rgb, K)

    #hello = rgb.astype(np.uint8).copy() 
    #hello = cv2.aruco.drawDetectedMarkers(hello,det_corners,ids)

    #rots,tvecs,img = aruco.FindPoses(K,camInfo.D,det_corners,hello,len(ids))
   
    #visu.plotImg(img)

    rospy.Subscriber(cameraName+"/rgb/image_color", Image, callback,(K,camInfo.D))

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()




if __name__ == '__main__':
    main()
