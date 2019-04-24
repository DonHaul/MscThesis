
import numpy as np

import synth

import rospy

import pickler as pickle

import matmanip as mmnip

import visu 

import ArucoInfoGetter

import random

import probdefs
import algos

import observationgenner as obsGen


from sensor_msgs.msg import Image

def main():

    showVideo = 1
    calc = 3  #0 is R 1 is t 2 is R for cameras, 4 is t for cameras

    

    camsName = ["abretesesamo","ervilhamigalhas"]

    rospy.init_node('my_name_is_jeff', anonymous=True)

    camInfo = pickle.Out("static/CameraInfo 20-04-2019.pickle")

    ig = ArucoInfoGetter.ArucoInfoGetter(camInfo['K'],camInfo['D'],showVideo,calc)
     
    # all of the parameters
    cb_params =	{"camId":0}
     # all of the functions
    cb_functions = []

    
    rospy.Subscriber(camsName[cb_params["camId"]]+"/rgb/image_color", Image, ig.callback,(cb_params,cb_functions))

    cb_params["camId"]=1
     # all of the functions
    cb_functions = []

    
    rospy.Subscriber(camsName[cb_params["camId"]]+"/rgb/image_color", Image, ig.callback,(cb_params,cb_functions))

    try:
        rospy.spin()
    except KeyboardInterrupt:
        print("shut")

    cv2.destroyAllWindows()



















if __name__ == '__main__':
    main()