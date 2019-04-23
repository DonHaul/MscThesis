#!/usr/bin/env python
# Software License Agreement (BSD License)
import numpy as np
import cv2
import pickler as pickle

import aruco #findPoses function is here

import rospy


from sensor_msgs.msg import Image
import rosinterface as roscv

import time

import synth #THIS IS HERE BECAUSE ROTATIONS ARE FAKE - DELETE IN FINAL VERSION - WRONG
import ArucoInfoGetter
import probdefs
import algos

import visu


def main():

    R,t = synth.FakeArucoReal() #<-- MUST BE REMOVED LATER

    #IMPORTING REAL ROTATIONS, SHOW WITH AND WITHOUT THIS
    ola = pickle.Out("static/ArucoRot.pickle")
    R =ola["RlocalPermutated"]

    
    cameraName = "abretesesamo"

    rospy.init_node('my_name_is_jeff', anonymous=True)

    camInfo = pickle.Out("static/CameraInfo 20-04-2019.pickle")

    showVideo = 1
    calc= 1  #0 is R 1 is t

    ig = ArucoInfoGetter.ArucoInfoGetter(camInfo['K'],camInfo['D'],showVideo,calc,R)

    # all of the parameters
    cb_params =	{}

     # all of the functions
    cb_functions = []

    rospy.Subscriber(cameraName+"/rgb/image_color", Image, ig.callback,(cb_params,cb_functions))


    try:
        rospy.spin()
    except KeyboardInterrupt:
        print("shut")

    cv2.destroyAllWindows()


    print("FINISHED")


    #A,b =  probdefs.translationProbDef(ig.obstList,R,12)
    #x = algos.LeastSquares(A,b)

    #THIS HAS 3 singular values that are pretty much zero
    #_,s,_ = np.linalg.svd(np.dot(A.T,A))
    #print(s)

    x = np.dot(np.linalg.pinv(ig.ATA),ig.ATb)
    
    print("sums")
    print(sum(x))

    solsplit2 = np.split(x,len(t))
    visu.ViewRefs(R,solsplit2,refSize=0.1)

    pickle.In("ArucoModel","R",R)
    pickle.In("ArucoModel","t",solsplit2)




if __name__ == '__main__':
    main()
