import rospy
import numpy as np
from sensor_msgs.msg import PointCloud2
from ast import literal_eval
import struct
from matplotlib import pyplot as plt
import rosinterface
import open3d
import pointclouder

rospy.init_node('my_name_is_jeff', anonymous=True)


cameraNames=["abretesesamo,ervilhamigalhas"]

topicDepth ="abretesesamo/depth_registered/points"

pcROSlist = []

pcs = []

for name in cameraNames:
    msg = rospy.wait_for_message(topicDepth, PointCloud2)

    pcrgb, pcpos =  rosinterface.pcROS2rgbpos(msg)
    
    pcs.append(pointclouder.Points2Cloud(pcpos,pcrgb))

#Rotate and trnaslate point clouds at this point

#see individual clouds
for pc in pcs:
    #see 1 clouds
    open3d.draw_geometries([pc])

#see all clouds
open3d.draw_geometries(pcs)

finalPc = pointclouder.MergeClouds(pcs)

