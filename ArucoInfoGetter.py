"""
ArucoInfoGetter.py

This module contains the a class that fetches the aruco and generates observations
And it calculates the problem definition as well
"""
import rosinterface as roscv
import numpy as np
import cv2
import aruco
import probdefs

import observationgenner as obsgen

class ArucoInfoGetter(object):
    def __init__(self,K,D,showVid=0,calc=0,R=None,Nmarkers=12,markerIDoffset=-2):
      
        
        self.Nmarkers = Nmarkers #number of markers, MUST BE CONTIGUOUS for this to work
        self.markerIDoffset=markerIDoffset #offset dos markers, como vao do 2 ao 12, o offset e 2

        #initialize A.TxA
        self.ATA = np.zeros((self.Nmarkers *3,self.Nmarkers *3)) #*3 because rotations matrix is 3x3
        #initialize A.Txb
        self.ATb = np.zeros((self.Nmarkers *3,1)) # *3 because tranlations are 3x1

        #intrinsic Params
        self.K = K

        #Distortion params
        self.D = D

        #show video
        self.showVid = showVid

        # 0 for rotation
        # 1 for translation 
        self.calc = calc

        #eventual R (if it exists), used on the translation part
        self.R = R

        self.img=[]

    def GetImg(self):
        return self.img

    def callback(self,data,args):
        '''callback called everytime a new image comes from ROS'''
                

        #fetches ros image
        img = roscv.rosImg2RGB(data)

        self.img = img

        #calculates rotations
        if (self.calc == 0):
            img,ids,obsR,obsT = aruco.ArucoObservationMaker(img,self.K,self.D,self.markerIDoffset,self.Nmarkers,captureR=True,captureT=False)

            
            obsgen.ObsViewer(obsR,pause=False)

            #only if there are observations it makes the A matrix
            if  ids is not None and len(ids)>1:
                A =  probdefs.rotationProbDef(obsR,self.Nmarkers)

                self.ATA = self.ATA + np.dot(A.T,A) #way to save the matrix in a compact manner

        #calculates translations
        elif (self.calc == 1):
            
            img,ids,obsR,obsT = aruco.ArucoObservationMaker(img,self.K,self.D,self.markerIDoffset,self.Nmarkers,captureR=True,captureT=True)
            
            if  ids is not None and len(ids)>1:
                A,b =  probdefs.translationProbDef(obsT,self.R,self.Nmarkers)

                self.ATA = self.ATA + np.dot(A.T,A) #way to save the matrix in a compact manner

                self.ATb = self.ATb + np.dot(A.T,b) #way to save the matrix in a compact manner


        #shiow video, or frame of just don't
        if(self.showVid == 1):
            cv2.imshow("Image window" , img)
            cv2.waitKey(3)
        elif(self.showVid == 2):
            cv2.imshow("Image window", img)
            cv2.waitKey(0)

        