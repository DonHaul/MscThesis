"""
observationgenner.py

This module contains functions that make pairs of observations
"""
import numpy as np
import matmanip as mmnip
import aruco
import cv2

import visu



def Cam2ArucoObsMaker(img,K,D,markerIDoffset,Nmarkers):
    '''
    this function creates observations between this camera and every aruco marker it sees

    if the camera sees markers 1 2 and 3

    it will generate Rcam_1 Rcam_2 and Rcam_3

    THIS FUNCTION WILL GENERATE SAMPLES FOR A SINGLE CAMERA
    
    Args:
        K - intrinsic camera matrix
        D - distortion parameters
        det_corners - all detected corners
        hello - image that has the aruco detections added to it on top
        ids - all detected ids

    Returns:
        observations (dict array):All marker observations made by this camera
            obsId: observed aruco marker
            t: translation from obsId to camera (marker position in world coordinates)
            R: rotation from camera to obsId
    '''
    
    #fetches detected markers
    det_corners, ids, rejected = aruco.FindMarkers(img, K)

    #changes image
    hello = img.astype(np.uint8).copy() 
    hello = cv2.aruco.drawDetectedMarkers(hello,det_corners,ids)
    
    #list of all observations generated
    observations =[]

    #if more than one marker was detected
    if  ids is not None and len(ids)>1:

        #finds rotations and vectors and draws referentials on image
        rots,tvecs,img = aruco.FindPoses(K,D,det_corners,hello,len(ids))

        #squeeze
        ids = ids.squeeze()


        #generates samples
        for i in range(0,len(ids)):                
                 
                 #only valid markers
                if i not in range(2,14):
                    #print("Invalid marker id: "+str(i))
                    continue 

                #initializes observation
                o ={"obsId":i+markerIDoffset}

                #generate R observations
                o['R']=rots[i]

                #generate t observations
                o['t']=np.squeeze(tvecs[i]) #WRONG - Not sure if this is the correct t
                
                observations.append(o)
 
    return observations ,img


def GenerateCameraPairObs(camsObs,R,t):
    '''
    Generate observations between 2 cameras, by doing Transformations throught the aruco

    camObs (list of list of dicts) - first list dimensions tells us the camera, the second list is all the observations for that camera
    R - rotations of the aruco model
    t - translation of the aruco model
    '''

    #initialize observation lists
    obsR = []
    obsT = []


    #this double for loop makes all camera combinations
    #between one camera
    for i in range(0,len(camsObs)):
        #and another camera
        for j in range(i+1,len(camsObs)):
            
            #this double loop matches every possible observation in each camera        
            #go through all the obs of one camera
            for obsiR in camsObs[i]:
                #and through all the obs of the other
                for obsjR in camsObs[j]:
                
                    #confusing as fuck i, know
                    # pretty much we have Rcam_i -> obsId_i and Rcam_j -> obsId_j   - to what each camera is observating is alwaying
                    # 'ObsId' = 'to' , and the cameraId on the array is the 'from'
                    
                    #print("from camera:"+str(j)+" to camera:"+str(i))
                    #print(np.linalg.multi_dot([obsiR['R'].T,R[obsiR['obsId']],R[obsjR['obsId']].T,obsjR['R']]))
                    #raw_input()

                    obsR.append({"from":j,"to":i,"R": np.linalg.multi_dot([obsiR['R'].T,R[obsiR['obsId']],R[obsjR['obsId']].T,obsjR['R']])})


                    
                    #AND MATCHERU THEM

                    #confusing as fuck i, know
                    # pretty much we have Rcam_i -> obsId_i and Rcam_j -> obsId_j   - to what each camera is observating is alwaying
                    # 'ObsId' = 'to' , and the cameraId on the array is the 'from'
                    #Feito erradamente moreless empiricamente
                    Rbetweenaruco = np.dot(R[obsjR['obsId']],R[obsiR['obsId']].T)

                    #print("Rbetweenaruco")
                    #print(Rbetweenaruco.shape)
                    tbetweenaruco = np.dot(R[obsjR['obsId']].T, t[obsiR['obsId']] - t[obsjR['obsId']])
                    #print("tbetweenaruco")
                    #print(tbetweenaruco.shape)

                    #print("R[obsjR['obsId']].T")
                    #print(R[obsjR['obsId']].T.shape)

                    #print("t[obsiR['obsId']]")
                    #print(t[obsiR['obsId']].shape)

                    #print("t[obsjR['obsId']]")
                    #print(t[obsjR['obsId']].shape)

                    new_R = np.linalg.multi_dot([obsiR['R'].T,R[obsiR['obsId']],R[obsjR['obsId']].T])
                    
                    #print("obsiR['t']")
                    #print(obsiR['t'].shape)

                    #print("oako")
                    #print(mmnip.InvertT(Rbetweenaruco.T, tbetweenaruco).shape)
                    #print("obsiR['R']")
                    #print(obsiR['R'].shape)

                    new_t =  mmnip.Transform(mmnip.InvertT(Rbetweenaruco.T, tbetweenaruco),obsiR['R'],  obsiR['t'])
                    
                    tij = mmnip.Transform(mmnip.InvertT(new_R.T, new_t),obsjR['R'],obsjR['t'])

                    obsT.append({"from":i,"to":j,"t": tij})

    return obsR,obsT