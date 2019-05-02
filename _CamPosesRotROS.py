
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



from sensor_msgs.msg import Image

def main():

    #Load aruco Model
    arucoModel = pickle.Pickle().Out("static/ArucoModel 01-05-2019 15-38-20.pickle")

     
    visu.ViewRefs(arucoModel['R'],arucoModel['t'],refSize=0.1)

    showVideo = 1
    calc = 0  #0 is R 1 is t 2 is R for cameras, 4 is t for cameras


    camsName = ["abretesesamo","ervilhamigalhas","broken"]

    #create gather class
    g = gather.img_gather(len(camsName),arucoModel,calc)

    rospy.init_node('my_name_is_jeff', anonymous=True)

    camInfo =pickle.Pickle().Out("static/CameraInfo 20-04-2019.pickle")

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


    if(g.N_cams==2):
        B = g.lol/g.count
        print("2 CAMS")
        visu.ViewRefs([np.eye(3),B])
    
    print("global1")
    rotSols = algos.RProbSolv1(g.ATA,3,g.N_cams)
   
    visu.ViewRefs(rotSols)
    print("global2")
    #rotSols = algos.RProbSolv1(C,3,len(R))    
    #visu.ViewRefs(rotSols)
     
    
    print("local1")    
    rr = mmnip.genRotRelLeft(rotSols)
    visu.ViewRefs(rr)

    pickle.Pickle().In("CamRot","R",rr)
    

    

















if __name__ == '__main__':
    main()