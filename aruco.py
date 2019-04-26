"""
aruco.py

This module contains aruco marker detection stuff
"""
import cv2
import numpy as np

def ArucoObservationMaker(img,K,D,markerIDoffset,Nmarkers,captureR=True,captureT=False):
        
        det_corners, ids, rejected = FindMarkers(img, K)

        hello = img.astype(np.uint8).copy() 
        hello = cv2.aruco.drawDetectedMarkers(hello,det_corners,ids)




        obsR,obsT,hello = ObservationMaker(K,D,det_corners,hello,ids,markerIDoffset,captureR,captureT)
        


        return hello ,ids,obsR,obsT #<- ids parameter doenst need to be here - WRONG

def ObservationMaker(K,D,det_corners,img,ids,markerIDoffset,captureR=True,captureT=False):
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
        rots,tvecs,img = FindPoses(K,D,det_corners,img,len(ids))

        #squeeze
        ids = ids.squeeze()



        #generates samples
        for i in range(0,len(ids)):                
            for j in range(i+1,len(ids)):
                
                if j not in range(2,14) or i not in range(2,14):
                    continue

                #generate R observations
                if(captureR):
                    obsR={"from":(ids[i]+markerIDoffset),"to":(ids[j]+markerIDoffset),"R":np.dot(rots[i],rots[j].T)}
                    observationsR.append(obsR)
                    

                if(captureT):
                    #generate t observations
                    obsT={"from":(ids[i]+markerIDoffset),"to":(ids[j]+markerIDoffset),"t":np.squeeze(np.dot(rots[j].T,(tvecs[i]-tvecs[j]).T))} 

                    #print(obsT)

                    observationsT.append(obsT)

    #print(observationsR)

    return observationsR , observationsT ,img


def FindMarkers(img,K):
    
    adict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_ARUCO_ORIGINAL)
        
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    det_corners, ids, rejected  = cv2.aruco.detectMarkers(gray,dictionary=adict,cameraMatrix=K)

    return det_corners, ids, rejected


def FindPoses(K,D,det_corners,img,n):


    rvecs, tvecs, _ = cv2.aruco.estimatePoseSingleMarkers(det_corners,0.0875,K,D)

    #the third parameter is corner coordinates

    #if(len(ids)>0):
    #print("rotation")
    #print(rots[0])
    #print("position")
    #if(len(tvecs)>0):
    #    print("tvecs"+ str(len(tvecs)))
    #    print(tvecs)


    #for r in rvecs
    rots = []

    for i in range(n):

        #converts to 3x3
        elm,_ = cv2.Rodrigues(rvecs[i,0,:])
        cv2.Rodrigues(src=rvecs[i,0,:])
        rots.append(elm)

        #print("rotation_elm")
        #print(elm)
        #print("det")
        #print(np.linalg.det(elm))
        #draws axis
        img = cv2.aruco.drawAxis(img,K,D,elm,tvecs[i],0.1)

    ola = np.asarray(rots)

    return rots,tvecs,img