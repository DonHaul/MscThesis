"""
CamPoseGetter.py

This module contains the a class receives all the images and observations of the cameras, and calculates stuff with it
"""

import numpy as np
import cv2

from libs import *


class ArucoInfoGetterv3(object):
    def __init__(self,camName,arucoData,intrinsics,stateru):
        
        self.state = stateru

        self.camName = camName

        #Array where several camera images will be concatenated into
        self.images =  np.zeros((480,640,3),dtype=np.uint8)

        #list of empty lists where observations will be saved (first dim tells camera, second dim is the observations for that cam)
        self.Allobs = []

        #intrinsic Params
        self.intrinsics = intrinsics


        self.arucoData=arucoData


        self.Nmarkers = len(self.arucoData['ids'])

        self.count = 0

        if(self.state.state==0):
            print("R problem Definition")
        elif(self.state.state==1):
            print("t problem Definition")
        else:
            print("SOMETHING WENT WRONG")

        #A.T b initialized
        self.ATb = np.zeros((self.Nmarkers*3,1)) 


        self.lol=np.zeros((3,3))

        self.arucoData['idmap'] = self.markerIdMapper(arucoData['ids'])
        
    def markerIdMapper(self,arr):

        IdMap={}
       
        for i in range(0,len(arr)):
            IdMap[str(arr[i])]=i
       
        return IdMap
    
    def callback(self,data):

        print("callback: "+str(self.count))

        self.count = self.count + 1


        #fetches ros image
        img = IRos.rosImg2RGB(data)

        self.img = img

        img,ids,obsR,obsT = aruco.ArucoObservationMaker(img,self.intrinsics['K'][self.camName],self.intrinsics['D'][self.camName],self.Nmarkers,self.arucoData,captureR=True,captureT=True)
        
  

        #calculates rotations
        if self.state.state == 0:
            
            #only if there are observations it makes the A matrix
            if  ids is not None and len(ids)>1:
                
                

                A =  probdefs.rotationProbDef(obsR,self.Nmarkers)

                self.state.ATAR = self.state.ATAR  + np.dot(A.T,A)

        #calculates translations
        elif self.state.state == 1:
            
            
            if  ids is not None and len(ids)>1:

                A,b =  probdefs.translationProbDef(obsT,self.state.R,self.Nmarkers)

                self.state.ATAt = self.state.ATAt + np.dot(A.T,A) #way to save the matrix in a compact manner

                self.state.ATb = self.state.ATb + np.dot(A.T,b) #way to save the matrix in a compact manner

        else:
            print("This State does nothing")

        #clear observations
        self.Allobs = []

        #shiow video, or frame of just don't
        #if(self.state.showImg == True):
        cv2.imshow("Image window" , img)
        cv2.waitKey(1)



    def showImg(self):
        '''Displays images from all cameras
        '''
        
        cv2.imshow("Image window ",self.images)           
        cv2.waitKey(1)
        



        



    



            

            
            
        
        




   