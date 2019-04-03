#!/usr/bin/env python
# Software License Agreement (BSD License)
import numpy as np
import cv2
import pickler as pickle
import datetime
import aruco
import open3d
import Rtmat
import pprint


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
import camcalib as calib



class InfoGetter(object):



    def __init__(self):
      
        self.objectpoints =[]
        self.imagepoints = []


        


    def callback(self,data):

        #print(time.time())
        #rospy.loginfo(rospy.get_caller_id() + 'I heard it')
        img = roscv.rosImg2RGB(data)
                
      
        img,corners2, objp = calib.ChessCalib(img,(7,6),0.01225)

        self.objectpoints.append(objp)
        self.imagepoints.append(corners2)

       

        #shows video
        cv2.imshow("Image window", img)
        cv2.waitKey(3)



def main():

    ig = InfoGetter()

    rospy.init_node('my_name_is_jeff', anonymous=True)

    cameraName = "abretesesamo"

     #subscribe
    rospy.Subscriber(cameraName+"/rgb/image_color", Image, ig.callback)


    try:
        rospy.spin()
    except KeyboardInterrupt:
        print("shut")


    print(ig)



    cv2.destroyAllWindows()
    print(ig.imagePoints)

    h = 480
    w = 640

    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(ig.objectPoints,ig.imagePoints, (640,480),None,None)

    newcameramtx, roi=cv2.getOptimalNewCameraMatrix(mtx,dist,(w,h),0,(w,h))
    


    print(mtx)



if __name__ == '__main__':
    main()
