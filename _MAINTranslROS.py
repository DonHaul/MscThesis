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



def main():

    R,t = synth.FakeAruco() #<-- MUST BE REMOVED LATER

    ig = ArucoInfoGetter.ArucoInfoGetter()

    cameraName = "abretesesamo"

    camInfo = pickle.Out("static/CameraInfo 20-04-2019.pickle")

 

    # all of the parameters
    cb_params =	{
    "showVideo": 1,
    "K": camInfo['K'],
    "D": camInfo['D'],
    "R": R
}
     # all of the functions
    cb_functions = [aruco.ArucoObservationMaker,probdefs.translationProbDef,algos.LeastSquares]

    rospy.Subscriber(cameraName+"/rgb/image_color", Image, ig.callback,(cb_params,cb_functions))


    try:
        rospy.spin()
    except KeyboardInterrupt:
        print("shut")

    cv2.destroyAllWindows()


    print("FINISHED")

    x = np.dot(np.linalg.inv(ig.ATA),ig.ATb)

    solsplit2 = np.split(x,len(t))
    visu.ViewRefs(R,solsplit2)




if __name__ == '__main__':
    main()
