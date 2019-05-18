"""
CamPoseGetter.py

This module contains the a class receives all the images and observations of the cameras, and calculates stuff with it
"""

import numpy as np
import cv2
import aruco
import probdefs
import observationgenner as obsGen
import rosinterface as IRos


class ArucoInfoGetterv3(object):
    def __init__(self,camName,arucoData,intrinsics,stateru):
        
        self.showVid=0

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

        #calculates rotations
        if self.state.state == 0:

            img,ids,obsR,obsT = aruco.ArucoObservationMaker(img,self.intrinsics['K'][self.camName],self.intrinsics['D'][self.camName],self.Nmarkers,self.arucoData,captureR=True,captureT=False)

            
            #only if there are observations it makes the A matrix
            if  ids is not None and len(ids)>1:
                
                
                if self.Nmarkers==2:
                    A=probdefs.rotationProbDefN2(obsgen,self.Nmarkers)
                    count=count+1
                    self.state.ATAR = self.state.ATAR  + np.dot(A.T,A)
                else:
                    A =  probdefs.rotationProbDef(obsR,self.Nmarkers)

                    self.state.ATAR = self.state.ATAR  + np.dot(A.T,A)

        #calculates translations
        elif self.state.state == 1:
            
            img,ids,obsR,obsT = aruco.ArucoObservationMaker(img,self.intrinsics['K'][self.camName],self.intrinsics['D'][self.camName],self.Nmarkers,self.arucoData,captureR=True,captureT=True)
            
            if  ids is not None and len(ids)>1:

                A,b =  probdefs.translationProbDef(obsT,self.state.R,self.Nmarkers)

                self.state.ATAt = self.state.ATAt + np.dot(A.T,A) #way to save the matrix in a compact manner

                self.state.ATb = self.state.ATb + np.dot(A.T,b) #way to save the matrix in a compact manner

        else:
            print("This State does nothing")

        #clear observations
        self.Allobs = []

        #shiow video, or frame of just don't
        if(self.state.showImg == True):
            cv2.imshow("Image window" , img)
            cv2.waitKey(1)



    def showImg(self):
        '''Displays images from all cameras
        '''
        
        cv2.imshow("Image window ",self.images)           
        cv2.waitKey(1)
        

    def GatherImg(self,camId,img,obs):
        '''Gathers Images and observations from a specific camera

        Args:
            camId:from which camera this is coming
            img: the image that the camera is transmitting
            obs: the observations extracted from the image
        '''
        
        #set image
        self.images[0:480,camId*640:camId*640+640,0:3]=img
        
        #increment statistic
        self.gatherCounter[camId] = self.gatherCounter[camId] +1
        
        #set is as fetched
        self.gatherReady[camId]=1

        #get new observations of that camera
        self.Allobs[camId]=self.Allobs[camId] +obs  # WRONG SHOULD IT BE concantenate lists OR =?

        #if all camera have sent something
        if(np.sum(self.gatherReady)== self.N_cams):
            
            #Generate Pairs from all of the camera observations
            obsR , obsT = obsGen.GenerateCameraPairObs(self.Allobs,self.R,self.t)

            #rotation problem
            if self.calc == 0:

                A = probdefs.rotationProbDef(obsR,self.N_cams)
                self.ATA = self.ATA + np.dot(A.T,A)

                if(self.N_cams)==2:
                    self.lol = self.lol+probdefs.rotationProbDefN2(obsR,self.N_cams)
                    self.count=self.count+1
            
            #translation problem
            elif self.calc ==1:

                
                A,b =  probdefs.translationProbDef(obsT,self.Rcam,self.N_cams)

                self.ATA = self.ATA + np.dot(A.T,A)
                self.ATb = self.ATb + np.dot(A.T,b)

            #set them all as unready
            self.gatherReady = np.zeros((self.N_cams),dtype=np.uint8)

            #clear observations
            self.Allobs = [ [] for i in range(self.N_cams) ]


        



    



            

            
            
        
        




   