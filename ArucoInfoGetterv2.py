import rosinterface as roscv
import numpy as np
import cv2
import aruco
import probdefs
import observationgenner as obsGen



class ArucoInfoGetter(object):
    def __init__(self,K,D,camId=0,gather=None):
      
        self.count = 0
        self.Nmarkers = 12 #number of markers, MUST BE CONTIGUOUS for this to work
        self.markerIDoffset=-2 #offset dos markers, como vao do 2 ao 12, o offset e 2

        #intrinsic Params
        self.K = K
        #Distortion params
        self.D = D

        self.camId = camId

        self.gather = gather

        


    def callback(self,data,args):

        
        img = roscv.rosImg2RGB(data)
        
        obs, img = obsGen.Cam2ArucoObsMaker(img,self.K,self.D,self.markerIDoffset,self.Nmarkers)

        self.gather.GatherImg(self.camId,img,obs)
        

        if(self.camId==0):
                  
            self.gather.showImg()
