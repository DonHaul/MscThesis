#start scirpt after starting ros


import sys,getopt
import rospy
from optparse import OptionParser
import json

import numpy as np

import datetime

import message_filters
from sensor_msgs.msg import Image

import random

import CamPoseGetter

import cv2

import commandline
import StateManager

from libs import *

import matplotlib.pyplot as plt

def main(argv):

    freq=20

    camNames = IRos.getAllPluggedCameras()
    print(camNames)
        
    rospy.init_node('do_u_kno_di_wae', anonymous=True)
   

    camSub = []



    #getting subscirpters to use message fitlers on
    for name in camNames:
        camSub.append(message_filters.Subscriber(name+"/rgb/image_color", Image))
        camSub.append(message_filters.Subscriber(name+"/depth_registered/image_raw", Image))


    path = FileIO.CreateFolder('../ImageSets/Cams')

    #initializes class
    data={}
    data['path']=path
    data['camNames']=camNames
    print(path)
    pcer = PCGetter(data)

    ts = message_filters.ApproximateTimeSynchronizer(camSub,20, 1.0/freq, allow_headerless=True)
    ts.registerCallback(pcer.callback)

    print("Fetching Messages")    
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print("shut")


    cv2.destroyAllWindows()


class PCGetter(object):

    def __init__(self,data):
        print("initiated")


        self.data = data

        self.count = 0 

        for camName in self.data['camNames']:
            FileIO.CreateFolder(data['path']+'/'+camName,putDate=False)

    def callback(self,*args):


        rgb = IRos.rosImg2RGB(args[0])
        depth_reg = IRos.rosImg2Depth(args[1])

        for camId in range(0,len(self.data['camNames'])):


            img = IRos.rosImg2RGB(args[camId*2])
            depth = IRos.rosImg2Depth(args[camId*2+1])

            #save rgb image
            cv2.imwrite(self.data['path']+'/'+self.data['camNames'][camId]+'/'+'rgb_'+str(self.count) +'.png',img)

            #save depth image
            cv2.imwrite(self.data['path']+'/'+self.data['camNames'][camId]+'/'+'depth_'+str(self.count) +'.png',depth)

        self.count=self.count+1







if __name__ == '__main__':
    main(sys.argv[1:])