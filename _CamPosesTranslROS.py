
import numpy as np

import synth

import rospy

import pickler as pickle

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



from sensor_msgs.msg import Image

def main():

    #Load aruco Model
    arucoModel = pickle.Out("static/ArucoModel 23-04-2019 13-45-37.pickle")

    CameraPose = pickle.Out("static/CameraPoseR 25-04-2019 20-08-11.pickle")

    Rcam = CameraPose['R']

    #visu.ViewRefs(Rcam)

    showVideo = 1
    calc = 1  #0 is R 1 is t 2 is R for cameras, 4 is t for cameras



    camsName = ["abretesesamo","ervilhamigalhas"]

    #create gather class
    g = gather.img_gather(len(camsName),arucoModel,calc,Rcam)

    rospy.init_node('my_name_is_jeff', anonymous=True)

    camInfo = pickle.Out("static/CameraInfo 20-04-2019.pickle")

    arucoGetters=[]

    # all of the parameters
    cb_params =	{}
    # all of the functions
    cb_functions = []

    for i in range(0,len(camsName)):

        #initialize class for each camera
        ig = ArucoInfoGetter.ArucoInfoGetter(camInfo['K'],camInfo['D'],i,g)

        #saves it for some reason
        arucoGetters.append(ig)

        #subscribe to each camera
        rospy.Subscriber(camsName[i] + "/rgb/image_color", Image, ig.callback,(cb_params,cb_functions))


    try:
        rospy.spin()
    except KeyboardInterrupt:
        print("shut")

    cv2.destroyAllWindows()

    #print("PIXA")
    #print(g.ATA)
    #print(g.ATb)

        
    x = np.dot(np.linalg.pinv(g.ATA),g.ATb)
    


    solsplit2 = np.split(x,g.N_cams)
    visu.ViewRefs(Rcam,solsplit2,refSize=0.1)

    print(solsplit2[1]-solsplit2[0])


















if __name__ == '__main__':
    main()