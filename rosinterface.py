import rospy
import cv2
from cv_bridge import CvBridge
import numpy as np
from sensor_msgs.msg import Image

def FetchDepthRegisteredRGB(cameraName):
    rospy.init_node('my_name_is_jeff', anonymous=True)

    topicRGB = "/rgb/image_color"
    topicDepth ="/depth_registered/image_raw"


    rgb = rospy.wait_for_message(cameraName + topicRGB, Image)
    depth_registered = rospy.wait_for_message(cameraName + topicDepth, Image)
    
    return rgb,depth_registered



def rgbmatrixfix(rgb):


    r=rgb[:,:,0]

    g=rgb[:,:,1]

    b=rgb[:,:,2]

    newrgb = np.array([b,g,r])

    newrgb = np.transpose(newrgb,[1,2,0])

    return newrgb


def rosCam2RGB(rgbros,depthros):
    #bridge to convert ROS image into numpy array
    br = CvBridge()

    rgb = br.imgmsg_to_cv2(rgbros, desired_encoding="passthrough")
    depth = br.imgmsg_to_cv2(depthros, desired_encoding="passthrough")
    

    rgb= rgbmatrixfix(rgb)

    return rgb,depth

def GetRGBD(cameraName):

    rgbros,depthros = FetchDepthRegisteredRGB(cameraName)

    rgb,depth = rosCam2RGB(rgbros,depthros)
    return rgb,depth