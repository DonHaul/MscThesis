#!/usr/bin/env python

from sensor_msgs.msg import Image
import rospy
import cv2
from cv_bridge import CvBridge
def main():
    rgb,depth = FetchDepthRegisteredRGB("/abretesesamo")
    br = CvBridge()
    cv_image = br.imgmsg_to_cv2(rgb, desired_encoding="passthrough")
    cv2.imwrite("my name is jeff.png", cv_image)









def FetchDepthRegisteredRGB(cameraName):
    rospy.init_node('my_name_is_jeff', anonymous=True)

    topicRGB = "/rgb/image_color"
    topicDepth ="/depth_registered/image_raw"


    rgb = rospy.wait_for_message(cameraName + topicRGB, Image)
    depth_registered = rospy.wait_for_message(cameraName + topicDepth, Image)
    
    return rgb,depth_registered




if __name__ == '__main__':
    main()