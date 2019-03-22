#!/usr/bin/env python
# Software License Agreement (BSD License)
import numpy as np
import cv2

## Simple talker demo that listens to std_msgs/Strings published 
## to the 'chatter' topic

import rospy

from sensor_msgs.msg import CameraInfo
import rosinterface as roscv
import visu


def callback(data):
    rospy.loginfo(rospy.get_caller_id() + 'I heard %s', data.data)

def main():

    cameraName = "camera"
    rgb=0

    rospy.init_node('my_name_is_jeff', anonymous=True)
    camInfo = rospy.wait_for_message("/camera/rgb/camera_info", CameraInfo)
    #print(camInfo)
    rgb,depth = roscv.GetRGBD(cameraName)
    #asdasd
    # fx 0  cx
    # 0  fy cy
    # 0  0  1

    K = np.asarray(camInfo.K).reshape((3,3))

    print(K)
 
    #print(rgb)

    #visu.plotImg(rgb)
    
    adict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_ARUCO_ORIGINAL)
    
    print("Marker Size", adict.markerSize)

    lolrgb = rgb.astype(np.uint8).copy() 
    gray = cv2.cvtColor(rgb, cv2.COLOR_BGR2GRAY)
    det_corners, ids, rejected  = cv2.aruco.detectMarkers(gray,dictionary=adict,cameraMatrix=K)
    hello = cv2.aruco.drawDetectedMarkers(lolrgb,det_corners,ids)
    print(det_corners)
    print(ids)   
    visu.plotImg(hello)

    print("lol")
    #rospy.Subscriber('chatter', String, callback)

    # spin() simply keeps python from exiting until this node is stopped
    # rospy.spin()




if __name__ == '__main__':
    main()
