#start scirpt after starting ros

import time
import sys,getopt
import rospy
from optparse import OptionParser
import json

import numpy as np

import datetime

import message_filters


import random

import CamPoseGetter

import cv2

import commandline
import zStateManager as StateManager

from libs import *

import matplotlib.pyplot as plt

import ImgStreamReader
import RosStreamReader

import zThread as commandline1

import threading

def worker(streamreader,stop):


    while(1==1):
        if(streamreader.nextIsAvailable):
            print("JERK5")
            streamreader.nextIsAvailable=False
            print(stop())
        if stop(): 
            break           
            



def main(argv):

    data =  FileIO.getJsonFromFile(argv[0])
    print(data)

    stop_threads = False

    



    state= StateManager.State()

    print("YEEEEEEEEEEEEEEEEEET")
    #sets thread where state changer will be
    t1 = threading.Thread(target=worker,args=( state,lambda : stop_threads))
    t1.start()

    #HAS TO BE AFTER
    #imgStream = ImgStreamReader.ImgStreamReader(data['input']['path'])
    imgStream = RosStreamReader.RosStreamReader(state)

    




    print("BIIIIG BOYYYYY")
    stop_threads = True
    t1.join() 
    


def imgShower(data):

    rows=1
    colunms=len(data['rgb'])
    
    if len(data['depth'])>0:
        rows=rows+1
    
    shape = data['rgb'][0].shape
    imgs =  np.zeros((shape[0]*rows,shape[1]*colunms,3),dtype=np.uint8)



    for i in range(colunms):
        imgs[0:shape[0],shape[1]*i:shape[1]*(i+1),0:3]=data['rgb'][i]
        #imgs[shape[0]*1:shape[0]*(1+1),shape[1]*i:shape[1]*(i+1),0:3]=data['depth'][i]



    cv2.imshow('image',imgs)
    cv2.waitKey(10)
    




    



if __name__ == '__main__':
    main(sys.argv[1:])