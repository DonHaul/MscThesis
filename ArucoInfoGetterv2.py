"""
ArucoInfoGetterv2.py

This module contains the a class that fetches the aruco and generates observations 
"""
import rosinterface as roscv
import numpy as np
import aruco
import observationgenner as obsGen



class ArucoInfoGetter(object):
    def __init__(self,K,D,camId=0,gather=None,Nmarkers=12,markerOffset = -2):
      
        
        self.Nmarkers = Nmarkers #number of markers, MUST BE CONTIGUOUS for this to work
        self.markerIDoffset=markerOffset #offset dos markers, como vao do 2 ao 12, o offset e 2

        #intrinsic Params
        self.K = K

        #Distortion params
        self.D = D

        #camera Id of the camera this class instance is attributed to
        self.camId = camId

        #gather class that mashes all of them
        self.gather = gather

        
    def callback(self,data,args):
        '''Callback called upon new message arrives on ROS
        
        Args:
            data: data on that message
            args: arguments I dont actually need and should delete
        '''
        
        #get image
        img = roscv.rosImg2RGB(data)
        
        #get observations of this camera, and image with the detected markers and referentials shown
        obs, img = obsGen.Cam2ArucoObsMaker(img,self.K,self.D,self.markerIDoffset,self.Nmarkers)

        #transmit image and observations to gatherer
        self.gather.GatherImg(self.camId,img,obs)
        
        #only if this is camera 0, refresh the show image
        #this is only done on 1 camera, because if done on several, it would break everything
        if(self.camId==0):
            self.gather.showImg()
