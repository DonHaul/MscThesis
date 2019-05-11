
import numpy as np

import synth

import rospy

import pickler2 as pickle

import matmanip as mmnip

import visu 

import ArucoInfoGetterv2 as ArucoInfoGetter

import random

import probdefs
import algos

import observationgenner as obsGen

import img_gatherer as gather

import cv2

import visu

import message_filters

from sensor_msgs.msg import Image

import message_filters

def callback2(*img):
    print("YUP IT WAS SYNCED")
    #print(img1.header.stamp)
    #print(img2.header.stamp)
    #print(img3)
    

def main():

    #Load aruco Model
    arucoModel = pickle.Pickle().Out("static/ArucoModel 01-05-2019 15-38-20.pickle")

     
    showVideo = 1
    calc = 0  #0 is R 1 is t 2 is R for cameras, 4 is t for cameras


    camsName = ["abretesesamo","ervilhamigalhas","broken"]

    #create gather class
    #g = gather.img_gather(len(camsName),arucoModel,calc)

    rospy.init_node('my_name_is_jeff', anonymous=True)

    
    #camInfo =pickle.Pickle().Out("static/CameraInfo 20-04-2019.pickle")

    #arucoGetters=[]

    # all of the parameters
    #cb_params =	{}
    # all of the functions  
    #cb_functions = []

    #for i in range(0,len(camsName)):

        #initialize class for each camera
        #ig = ArucoInfoGetter.ArucoInfoGetter(camInfo['K'],camInfo['D'],i,g)

        #saves it for some reason
        #arucoGetters.append(ig)

        #subscribe to each camera
        #rospy.Subscriber(camsName[i] + "/rgb/image_color", Image, ig.callback,(cb_params,cb_functions))

    image_sub1 = message_filters.Subscriber(camsName[0]+"/rgb/image_color", Image)
    image_sub2 = message_filters.Subscriber(camsName[1]+"/rgb/image_color", Image)

    freq=400

    # all of the parameters
    cb_params =	{}
     # all of the functions
    cb_functions = []

    ts = message_filters.ApproximateTimeSynchronizer([image_sub1, image_sub2],10, 1.0/freq, allow_headerless=True)
    ts.registerCallback(callback2,(cb_params,cb_functions))


    try:
        rospy.spin()
    except KeyboardInterrupt:
        print("shut")

    cv2.destroyAllWindows()


    

















if __name__ == '__main__':
    main()