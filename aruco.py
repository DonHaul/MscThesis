"""
aruco.py

This module contains aruco marker detection stuff
"""
import cv2
import numpy as np

def ArucoObservationMaker(img,K,D,markerIDoffset,Nmarkers,captureR=True,captureT=False):
    '''
    Finds Markers and makes observations

    Args:
        img: image to find aruco markers in
        K: intrinsic parameters
        D: distortion parameters
        markerIDoffset: shift from lowest id to 0
        Nmarkers: number of existing markers
        captureR (Bool): whether or not will be generated rotation observations
        captureT (Bool): whether or not will be generated translation observations

    Returns: 
        hello: image with detected markers and their referentials
        ids: detected ids
        obsR: observated Rotations
        obsT: observated translations
    '''

    #finds markers
    det_corners, ids, rejected = FindMarkers(img, K)

    #copy image
    hello = img.astype(np.uint8).copy() 

    #draw maerkers
    hello = cv2.aruco.drawDetectedMarkers(hello,det_corners,ids)

    #make observations, and draw referentials
    obsR,obsT,hello = ObservationMaker(K,D,det_corners,hello,ids,markerIDoffset,captureR,captureT)

    return hello ,ids,obsR,obsT #<- ids parameter doenst need to be here - WRONG

def ObservationMaker(K,D,det_corners,img,ids,markerIDoffset,captureR=True,captureT=False):
    '''
    Generates Observations

    Args:
        K: intrinsic camera matrix
        D: distortion parameters
        det_corners: all detected corners
        hello: img
        ids: all detected ids
    Returns:
        observationsR: rotation observations
        observationsT: tranlation observations
        img: img with markers and referentials in it
    '''
    
    observationsR = []
    observationsT = []

    #if more than one marker was detected
    if  ids is not None and len(ids)>1:

        #finds rotations and vectors and draws referentials on image
        rots,tvecs,img = FindPoses(K,D,det_corners,img,len(ids))
        #this rots and tvecs are in camera coordinates

        #squeeze
        ids = ids.squeeze()



        #generates samples
        for i in range(0,len(ids)):                
            for j in range(i+1,len(ids)):
                
                if ids[j] not in range(2,14) or ids[i] not in range(2,14):
                    continue

                #print("observing "+str(i)+" and "+str(j))

                #generate R observations
                if(captureR):
                    obsR={"to":(ids[i]+markerIDoffset),"from":(ids[j]+markerIDoffset),"R":np.dot(rots[i].T,rots[j])}
                    observationsR.append(obsR)
                
                
                if(captureT):
                    #generate t observations
                    obsT={"from":(ids[i]+markerIDoffset),"to":(ids[j]+markerIDoffset),"t":np.squeeze(np.dot(rots[j].T,(tvecs[i]-tvecs[j]).T))} 
                    observationsT.append(obsT)

    return observationsR , observationsT ,img


def FindMarkers(img,K):
    '''Detects aruco markers in an image

    Args:
        img: image to extract markers from
        K: camera intrinsic parameters
    '''  

    #What type of aruco markers are there
    adict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_ARUCO_ORIGINAL)

    #make the image grey
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    #get markers
    det_corners, ids, rejected  = cv2.aruco.detectMarkers(gray,dictionary=adict,cameraMatrix=K)

    return det_corners, ids, rejected


def FindPoses(K,D,det_corners,img,n):
    '''
    Estimates rotation and translation of each aruco

    Args:
        K: intrinsic parameters
        D: distortion parameters
        det_corners:detected corners
        img: image to draw axis on
        n: number of detected ids
    '''

    #get pose
    rvecs, tvecs, _ = cv2.aruco.estimatePoseSingleMarkers(det_corners,0.0875,K,D)

    #the third parameter is corner coordinates


    #for r in rvecs
    rots = []

    for i in range(n):

        #converts to 3x3 rotation matrix
        elm,_ = cv2.Rodrigues(rvecs[i,0,:])
        cv2.Rodrigues(src=rvecs[i,0,:])
        rots.append(elm)

        #draws axis
        img = cv2.aruco.drawAxis(img,K,D,elm,tvecs[i],0.1)

    ola = np.asarray(rots)

    return rots,tvecs,img