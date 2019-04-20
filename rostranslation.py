#!/usr/bin/env python
# Software License Agreement (BSD License)
import numpy as np
import cv2
import pickler as pickle

import aruco #findPoses function is here

import rospy

from sensor_msgs.msg import CameraInfo
from sensor_msgs.msg import Image
import rosinterface as roscv

import time

import synth #THIS IS HERE BECAUSE ROTATIONS ARE FAKE - DELETE IN FINAL VERSION - WRONG
import ArucoInfoGetter
import probdefs
import algos



def main():

    R,t = synth.FakeAruco()

    ig = ArucoInfoGetter.ArucoInfoGetter()

    cameraName = "abretesesamo"

    rospy.init_node('my_name_is_jeff', anonymous=True)


    #fetch intrinsic parameters
    camInfo = rospy.wait_for_message("/"+cameraName + "/rgb/camera_info", CameraInfo)        

    rgb,depth = roscv.GetRGBD(cameraName)    
    #print(camInfo)
    K = np.asarray(camInfo.K).reshape((3,3))
    #print(K)
    #pickle.In("CameraInfo","K",K)
    #pickle.In("CameraInfo","dist",camInfo.D) 
    #subscribe

    # all of the parameters
    cb_params =	{
    "showVideo": 1,
    "K": K,
    "D": camInfo.D,
    "R": R
}
     # all of the functions
    cb_functions = [ArucoObservationMaker,probdefs.translationProbDef,algos.LeastSquares]

    rospy.Subscriber(cameraName+"/rgb/image_color", Image, ig.callback,(cb_params,cb_functions))


    try:
        rospy.spin()
    except KeyboardInterrupt:
        print("shut")

    cv2.destroyAllWindows()


    print("FINISHED")


def ObservationMaker(K,D,det_corners,hello,ids,markerIDoffset):
    '''
    K - intrinsic camera matrix
    D - distortion parameters
    det_corners - all detected corners
    hello - img
    ids - all detected ids
    '''

    observationsR = []
    observationsT = []

    #if more than one marker was detected
    if  ids is not None and len(ids)>1:

        #finds rotations and vectors and draws referentials on image
        rots,tvecs,img = aruco.FindPoses(K,D,det_corners,hello,len(ids))

        #squeeze
        ids = ids.squeeze()

        #generates samples
        for i in range(0,len(ids)):                
            for j in range(i+1,len(ids)):

                #generate R observations
                obs={"from":(ids[i]+markerIDoffset),"to":(ids[j]+markerIDoffset),"R":np.dot(rots[i],rots[j].T)}
                observationsR.append(obs)

                #generate t observations
                obs={"from":(ids[i]+markerIDoffset),"to":(ids[j]+markerIDoffset),"t":np.dot(rots[i],rots[j].T)}
                observationsT.append(obs)

            

    return observationsR , observationsT

def ArucoObservationMaker(img,K,D,markerIDoffset,Nmarkers):
        
        det_corners, ids, rejected = aruco.FindMarkers(img, K)

        hello = img.astype(np.uint8).copy() 
        hello = cv2.aruco.drawDetectedMarkers(hello,det_corners,ids)




        obsR,obsT = ObservationMaker(K,D,det_corners,img,ids,markerIDoffset)
        


        return hello ,ids #<- ids parameter doenst need to be here - WRONG





if __name__ == '__main__':
    main()
