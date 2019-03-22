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

from sensor_msgs.msg import CameraInfo
import rosinterface as roscv
import visu

import time

def callback(data):
    rospy.loginfo(rospy.get_caller_id() + 'I heard %s', data.data)

def main():

    datdata={}

    cameraName = "camera"
    rgb=0

    rospy.init_node('my_name_is_jeff', anonymous=True)
    camInfo = rospy.wait_for_message("/camera/rgb/camera_info", CameraInfo)
    print(camInfo)
    
    rgb,depth = roscv.GetRGBD(cameraName)
    #asdasd
    # fx 0  cx
    # 0  fy cy
    # 0  0  1
    
    K = np.asarray(camInfo.K).reshape((3,3))

    det_corners, ids, rejected = aruco.FindMarkers(rgb, K)

    hello = rgb.astype(np.uint8).copy() 
    hello = cv2.aruco.drawDetectedMarkers(hello,det_corners,ids)

    rots,tvecs,img = aruco.FindPoses(K,camInfo.D,det_corners,hello,len(ids))
   
    visu.plotImg(img)

    #rospy.Subscriber('chatter', String, callback)

    # spin() simply keeps python from exiting until this node is stopped
    # rospy.spin()




if __name__ == '__main__':
    main()
