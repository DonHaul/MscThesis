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
    cb_functions = [ArucoObservationMaker,probdefs.translationProbDef,algos.LeastSquares]

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
                obsR={"from":(ids[i]+markerIDoffset),"to":(ids[j]+markerIDoffset),"R":np.dot(rots[i],rots[j].T)}
                observationsR.append(obsR)

                #generate t observations
                obsT={"from":(ids[i]+markerIDoffset),"to":(ids[j]+markerIDoffset),"t":np.dot(rots[i],rots[j].T)} #<-- WRONG
                observationsT.append(obsT)

            

    return observationsR , observationsT

def ArucoObservationMaker(img,K,D,markerIDoffset,Nmarkers):
        
        det_corners, ids, rejected = aruco.FindMarkers(img, K)

        hello = img.astype(np.uint8).copy() 
        hello = cv2.aruco.drawDetectedMarkers(hello,det_corners,ids)




        obsR,obsT = ObservationMaker(K,D,det_corners,img,ids,markerIDoffset)
        


        return hello ,ids,obsR,obsT #<- ids parameter doenst need to be here - WRONG





if __name__ == '__main__':
    main()
