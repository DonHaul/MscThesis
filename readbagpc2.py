#!/usr/bin/python

#usage  python readbagpc2.py <bag file> <>

import sys
import open3d
import converter
import cv2

print 'Number of arguments:', len(sys.argv), 'arguments.'
print 'Argument List:', str(sys.argv)

import rosbag
import rospy
from sensor_msgs.msg import PointCloud2
import numpy as np
from cv_bridge import CvBridge

br = CvBridge()

bag = rosbag.Bag(sys.argv[1])

count = 0
where = 2

topicRGB ='/camera/rgb/image_color'
topicDepth = '/camera/depth/image'
topicPC = '/camera/rgb/points'

clouds =[]

for topic, msg, t in bag.read_messages(topics=[topicPC,'/tf',topicDepth,topicRGB]):

    count=count+1

    if count >= where:
        if topic== topicRGB:
            cv_image = br.imgmsg_to_cv2(msg, desired_encoding="passthrough")
            cv2.imwrite("this_was_a_message_briefly.png", cv_image)

            break
        if topic== topicDepth:
            cv_image = br.imgmsg_to_cv2(msg, desired_encoding="passthrough")
            cv2.imwrite("this_was_a_message_briefly2.png", cv_image)
        if topic== topicPC:
            pc = converter.PC2toOpen3DPC(msg)
            clouds.append(pc)

    elif count > where:
        break


bag.close()

open3d.draw_geometries(clouds)