#!/usr/bin/env python
# Software License Agreement (BSD License)
import numpy as np
import cv2
import pickler as pickle
import datetime
import aruco


## Simple talker demo that listens to std_msgs/Strings published 
## to the 'chatter' topic

import rospy
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import CameraInfo
from sensor_msgs.msg import Image
import rosinterface as roscv
import visu

import time



class InfoGetter(object):
    def __init__(self):
      
        self.count = 0

        


    def callback(self,data,args):

        K=args[0]
        D=args[1]
        
        self.count = self.count +1

        #print(time.time())
        #rospy.loginfo(rospy.get_caller_id() + 'I heard it')
        img = roscv.rosImg2RGB(data)
        
        det_corners, ids, rejected = aruco.FindMarkers(img, K)

        hello = img.astype(np.uint8).copy() 
        hello = cv2.aruco.drawDetectedMarkers(hello,det_corners,ids)

        
        if  ids is not None:
            rots,tvecs,img = aruco.FindPoses(K,D,det_corners,hello,len(ids))

    

        #cv2.imshow("Image window", img)
        #cv2.waitKey(3)
        #bridge = CvBridge()

        #try:
        #  cv_image = bridge.imgmsg_to_cv2(data, "bgr8")
        #except CvBridgeError as e:
        #  print(e)

        print(self.count)

        cv2.imshow("Image window", hello)
        cv2.waitKey(0)

    

def main():

    global count
    count = 0
    datdata={}

    ig = InfoGetter()

    cameraName = "abretesesamo"
    rgb=0

    rospy.init_node('my_name_is_jeff', anonymous=True)
    camInfo = rospy.wait_for_message("/"+cameraName + "/rgb/camera_info", CameraInfo)
        
    rgb,depth = roscv.GetRGBD(cameraName)
    
    K = np.asarray(camInfo.K).reshape((3,3))

    #det_corners, ids, rejected = aruco.FindMarkers(rgb, K)

    #hello = rgb.astype(np.uint8).copy() 
    #hello = cv2.aruco.drawDetectedMarkers(hello,det_corners,ids)

    #rots,tvecs,img = aruco.FindPoses(K,camInfo.D,det_corners,hello,len(ids))
   
    #visu.plotImg(img)

    rospy.Subscriber(cameraName+"/rgb/image_color", Image, ig.callback,(K,camInfo.D))

    # spin() simply keeps python from exiting until this node is stopped
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print("Shutting down")
    cv2.destroyAllWindows()




if __name__ == '__main__':
    main()
