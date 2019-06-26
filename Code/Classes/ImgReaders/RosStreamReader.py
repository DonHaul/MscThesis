
import numpy as np
import cv2
from libs import *

import message_filters

import os

from sensor_msgs.msg import Image

import threading

import rospy

import StreamReader

class RosStreamReader(StreamReader.StreamReader):

    
    def __init__(self,camNames=None,freq=20):

        StreamReader.StreamReader.__init__(self)

        self.freq = freq

        self.camNames=camNames

        if len(self.camNames)==0:
            self.camNames = IRos.getAllPluggedCameras()

        
        self.N_cams = len(self.camNames)

        self.data={'names':self.camNames,'rgb':[],'depth':[]}

        self.nextIsAvailable=False

        


        rospy.init_node('do_u_kno_di_wae', anonymous=True)
        
        camSub = []

        #getting subscirpters to use message fitlers on
        for name in self.camNames:
            camSub.append(message_filters.Subscriber(name+"/rgb/image_color", Image))
            camSub.append(message_filters.Subscriber(name+"/depth_registered/image_raw", Image))




        ts = message_filters.ApproximateTimeSynchronizer(camSub,20, 1.0/freq, allow_headerless=True)
        ts.registerCallback(self.callback)

        


    def callback(self,*args):

        data={'names':self.camNames,'rgb':[],'depth':[]}
        #print("NEXTU DES")
        #print(self.N_cams)
        for camId in range(0,self.N_cams):
            img = IRos.rosImg2RGB(args[camId*2])
            depth = IRos.rosImg2Depth(args[camId*2+1])

            data['rgb'].append(img)
            data['depth'].append(depth)
    
        self.data=data
        self.nextIsAvailable=True


    def next(self):
        

        #print(type(RosStreamReadear))
        self.nextIsAvailable=False # this should be replaced by the next line
        #super(RosStreamReadear,self).next()

        return self.data      

