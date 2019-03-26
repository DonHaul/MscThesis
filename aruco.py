import cv2
import numpy as np

def FindMarkers(img,K):
    
    adict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_ARUCO_ORIGINAL)
        
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    det_corners, ids, rejected  = cv2.aruco.detectMarkers(gray,dictionary=adict,cameraMatrix=K)

    return det_corners, ids, rejected


def FindPoses(K,D,det_corners,img,n):

    #VVERIFY THAT VALUE TODO DANGER, MUST BE CORRECT LENGHT IN METERS 0.185
    rvecs, tvecs, obj = cv2.aruco.estimatePoseSingleMarkers(det_corners,0.0875,K,(0,0,0,0))

    #for r in rvecs
    rots = []

    for i in range(n):

        #converts to 3x3
        elm,_ = cv2.Rodrigues(rvecs[i,0,:])
        cv2.Rodrigues(src=rvecs[i,0,:])
        rots.append(elm)

        #draws axis
        img = cv2.aruco.drawAxis(img,K,D,elm,tvecs[i],0.1)

    ola = np.asarray(rots)

    return rots,tvecs,img