"""
CamPoseGetter.py

This module contains the a class receives all the images and observations of the cameras, and calculates stuff with it
"""

import numpy as np
import cv2
from libs import *


class CamPoseGetter(object):
    def __init__(self,camNames,arucoData,arucoModel,intrinsics,stateru):
        
        self.state = stateru

        self.R2=np.zeros((3,3))


        self.t2=np.zeros((3,1))

        #number of camera
        self.N_cams = len(camNames)

        self.camNames = camNames

        #Array where several camera images will be concatenated into
        self.images =  np.zeros((480,640*self.N_cams,3),dtype=np.uint8)

        #list of empty lists where observations will be saved (first dim tells camera, second dim is the observations for that cam)
        self.Allobs = [ [] for i in range(self.N_cams) ]

        #intrinsic Params
        self.intrinsics = intrinsics

        self.arucoData=arucoData
        self.arucoModel = arucoModel
        
        self.R = arucoModel['R']
        self.t = arucoModel['T']


        self.count = 0

        #for tt in arucoModel['t']:
        #    self.t.append(np.squeeze(tt))

        #Array where several camera images will be concatenated into
        self.images =  np.zeros((480,640*self.N_cams,3),dtype=np.uint8)

       


        #A.T b initialized
        self.ATb = np.zeros((self.N_cams*3,1)) 


        self.lol=np.zeros((3,3))

        self.arucoData['idmap'] = self.markerIdMapper(arucoData['ids'])
        
    def markerIdMapper(self,arr):

        IdMap={}
       
        for i in range(0,len(arr)):
            IdMap[str(arr[i])]=i
       
        return IdMap
    
    def callback(self,*args):


        #print("callback: "+str(self.count))
        #print(self.state.readyToCapture)
        if(self.state.readyToCapture==False):
            return

        self.count = self.count + 1
        #print(self.N_cams)
        #print(len(args))
        #print(self.state.stateDict)

        #iterate throguh cameras
        for camId in range(0,self.N_cams):
            
            

            if  self.state.arucoDetection == "singular":

                img = IRos.rosImg2RGB(args[camId])

                #get observations of this camera, and image with the detected markers and referentials shown
                obs, img = obsgen.Cam2ArucoObsMaker2(img,self.intrinsics['K'][self.camNames[camId]],self.intrinsics['D'][self.camNames[camId]],self.arucoData)

            elif self.state.arucoDetection == "allforone":
                
                img = IRos.rosImg2RGB(args[camId])

                obs, img = obsgen.CamArucoPnPObsMaker(img,self.intrinsics['K'][self.camNames[camId]],self.intrinsics['D'][self.camNames[camId]],self.arucoData,self.arucoModel)
            elif self.state.arucoDetection == "depthforone":

                
                img = IRos.rosImg2RGB(args[camId*2])
                depth = IRos.rosImg2Depth(args[camId*2+1])
                obs, img = obsgen.CamArucoProcrustesObsMaker(img,self.intrinsics['K'][self.camNames[camId]],self.intrinsics['D'][self.camNames[camId]],self.arucoData,self.arucoModel,depth)
            
            else:
                print("Big Oopsie 5809447652")
                quit()




            #obs = obsGen.FilterGoodObservationMarkerIds(obs,self.R,self.t,len(self.arucoData['idmap']),t_threshold=0.05,R_threshold=0.5)

            #set image
            self.images[0:480,camId*640:camId*640+640,0:3]=img

            #get new observations of that camera
            self.Allobs[camId]=obs  # WRONG SHOULD IT BE concantenate lists OR =?


        #Generate Pairs from all of the camera observations
        obsR , obsT = obsgen.GenerateCameraPairObs(self.Allobs,self.R,self.t)

        for oR,oT in zip(obsR,obsT):

            self.state.recordedRs.append(oR['R'])
            self.state.recordedTs.append(oT['t'])

        #print(len(obsR))
        #rotation problem
        if self.state.state == 0:

            A = probdefs.rotationProbDef(obsR,self.N_cams)
            self.state.ATAR = self.state.ATAR + np.dot(A.T,A)

            if self.state.data['errorCalc']==True:
                self.state.data['Rs']=self.state.data['Rs'] + helperfuncs.extractKeyFromDictList(obsR,'R')
                

        
        #translation problem
        elif self.state.state ==1:

            
            A,b =  probdefs.translationProbDef(obsT,self.state.R,self.N_cams)

            self.state.ATAt = self.state.ATAt + np.dot(A.T,A)
            self.state.ATb = self.state.ATb + np.dot(A.T,b)
        else:
            print("This State does nothing")


        if(self.N_cams)==2 and len(obsR)>0:
            rrr,ttt = probdefs.ProbDefN2(obsR,obsT,self.N_cams)
            #print("moreless rotation:")
            #print(rrr/len(obsR))
            #print("moreless translation:")
            #print(ttt/len(obsT))
            self.state.R2 = self.state.R2 + rrr
            self.state.count=self.state.count+len(obsT)
            self.state.t2 = self.state.t2 + ttt

            


        #clear observations
        self.Allobs = [ [] for i in range(self.N_cams) ]

        if self.state.showImg==True:
            self.showImg(self.state.detectionMode)

        if self.state.detectionMode=="snap":
            self.state.snapcount=self.state.snapcount-1
            
            if self.state.snapcount<=0:
                print("NO MAS")
                self.state.readyToCapture=False


    def showImg(self,mode):
        '''Displays images from all cameras
        '''
        
        cv2.imshow("Image window ",self.images)           
        
        if(mode=="snap"):
            cv2.waitKey(0)

        if mode=="realtime":
            cv2.waitKey(1)

        if(mode=="snap"):
            cv2.destroyAllWindows()
        



        



    



            

            
            
        
        




   