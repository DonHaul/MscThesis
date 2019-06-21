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
import GetCangalhoPoses

import CangalhoObservationsMaker

import zCommands as CommandLine

import zPosesCalculator as PosesCalculator

import threading

def worker(stream,obsmake,posecalc,stop):


    while(1==1):
       
        if stream.nextIsAvailable:

        
            stream.nextIsAvailable=False

            streamData= stream.next()

            if streamData is None:
                break

            img,ids,obsR,obsT = obsmake.GetObservations(streamData)

            posecalc.AddObservations(obsR,obsT)

        if stop(): 
            break           
            



def main(argv):

    #Reads the configuration file
    data =  FileIO.getJsonFromFile(argv[0])
    
    #variable that will stop all threads
    stop_threads = False

    #holds
    state= StateManager.State()

    imgStream={}
    ObservationMaker={}
    PosesCalculator={}

    #Assigns the InputStream
    if data['input']['type']=='IMG':
        imgStream = ImgStreamReader.ImgStreamReader(data['input']['path'])

        
    elif data['input']['type']=='ROS':
        imgStream = RosStreamReader.RosStreamReader()

    #setting stuff on state
    state.intrinsics = FileIO.getKDs(imgStream.camNames)
    state.arucodata = FileIO.getJsonFromFile(data['model']['arucodata'])

    singlecamData={"K":state.intrinsics['K'][imgStream.camNames[0]],"D":state.intrinsics['D'][imgStream.camNames[0]],"arucodata":state.arucodata}
    
    ObservationMaker =  CangalhoObservationsMaker.CangalhoObservationMaker(singlecamData)

    posedata={"N_objects":len(state.arucoData['ids'])}
    PosesCalculator = PosesCalculator.PosesCalculator(posedata)
    
    
    #GetPoses=GetCangalhoPoses.GetCangalhoPoses(singlecamData)
   
    t1 = threading.Thread(target=worker,args=( imgStream,ObservationMaker,PosesCalculator,lambda : stop_threads))
    t1.start()

    #sets thread where state changer will be
    CommandLine.Start(state,lambda : stop_threads)




    

    #if data['input']['type']=='ROS':
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print("shut")

    print("Exited Stuff")
    stop_threads = True
    t1.join() 

    print("YO MAMMA HAS THE BIG GAY")
    


def imgShower(data):

    rows=1
    colunms=len(data['rgb'])
    
    if len(data['depth'])>0:
        rows=rows+1
    
    shape = data['rgb'][0].shape
    imgs =  np.zeros((shape[0]*rows,shape[1]*colunms,3),dtype=np.uint8)



    for i in range(colunms):
        imgs[0:shape[0],shape[1]*i:shape[1]*(i+1),0:3]=data['rgb'][i]
        #imgs[shape[0]*1:shape[0]*(1+1),shape[1]*i:shape[1]*(i+1),0]=data['depth'][i]



    cv2.imshow('image',imgs)
    cv2.waitKey(10)
    




    



if __name__ == '__main__':
    main(sys.argv[1:])