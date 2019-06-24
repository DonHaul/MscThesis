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

import zStateManager as StateManager

from libs import *

import matplotlib.pyplot as plt


from Classes.ImgReaders import RosStreamReader,ImgStreamReader
from Classes.ObservationGenners import CamerasObservationMaker,CangalhoObservationsMaker
from Classes.ArucoDetecc import CangalhoPnPDetector,CangalhoProcrustesDetector,SingleArucosDetector
from Classes.PosesCalculators import PosesCalculator, OutlierRemPoseCalculator



import zCommands as CommandLine

import PosePipeline



import threading

def worker(posepipe):


    while True:
       
        if posepipe.imgStream.nextIsAvailable:

        
            posepipe.imgStream.nextIsAvailable=False

            streamData= posepipe.imgStream.next()

            if streamData is None:
                break

            img,ids,obsR,obsT = posepipe.ObservationMaker.GetObservations(streamData)

            posepipe.posescalculator.AddObservations(obsR,obsT)

            #print(posepipe.posescalculator.n_obs)


        if posepipe.GetStop(): 
            break           
            



def main(argv):

    

    #Reads the configuration file
    data =  FileIO.getJsonFromFile(argv[0])
    
    posepipeline = PosePipeline.PosePipeline()

    #holds
    state= StateManager.State()

    posepipeline.folder = FileIO.CreateFolder("./PipelineLogs/"+FileIO.GetAnimalName())


    arucodetectors={
        'singular':SingleArucosDetector.SingleArucosDetector,
        'allforone':CangalhoPnPDetector.CangalhoPnPDetector,
        'depthforone':CangalhoProcrustesDetector.CangalhoProcrustesDetector        }
    

    #Assigns the InputStream
    if data['input']['type']=='IMG':
        posepipeline.imgStream = ImgStreamReader.ImgStreamReader(data['input']['path'])
    elif data['input']['type']=='ROS':

        camNames = []

        if "cameras" in data['model']:
            camNames = data['model']['cameras'] 
        posepipeline.imgStream = RosStreamReader.RosStreamReader(camNames=camNames)
    else:
        print("This Pipeline input is invalid")

    #setting stuff on state
    state.intrinsics = FileIO.getKDs(posepipeline.imgStream.camNames)
    state.arucodata = FileIO.getJsonFromFile(data['model']['arucodata'])
    state.arucomodel = FileIO.getFromPickle(data['model']['arucomodel'])

    if data['model']['type']=='CANGALHO':
        
        singlecamData={
            "K":state.intrinsics['K'][imgStream.camNames[0]],
            "D":state.intrinsics['D'][imgStream.camNames[0]],
            "arucodata":state.arucodata}
        posepipeline.ObservationMaker =  CangalhoObservationsMaker.CangalhoObservationMaker(singlecamData)

        posedata={"N_objects":len(state.arucodata['ids'])}
        posepipeline.posescalculator = PosesCalculator.PosesCalculator(posedata)


    elif data['model']['type']=='CAMERA':
        multicamData={
            "intrinsics":state.intrinsics,
            "arucodata":state.arucodata,
            "camnames":posepipeline.imgStream.camNames,
            "arucomodel":state.arucomodel,
            "innerpipeline":{
                "arucodetector":arucodetectors[data['model']['arucodetection']]({'arucodata':state.arucodata,'arucomodel':state.arucomodel})
            }
            }
        
        posepipeline.ObservationMaker = CamerasObservationMaker.CamerasObservationMaker(multicamData)


        posedata={
            "N_objects":len(posepipeline.imgStream.camNames),
            "record":data["model"]["record"]}
        

        if data['model']['mode']['type']=='REGULAR':
            posepipeline.posescalculator = PosesCalculator.PosesCalculator(posedata)
        
        elif data['model']['mode']['type']=='OUTLIERREMOVE':
            posedata['observations']=data['model']['mode']['observations']
            posepipeline.posescalculator = OutlierRemPoseCalculator.OulierRemovalPoseCalculator(posedata)

        else:
            print("This pose calculator is invalid")

    else:
        print("This Pipeline Model is invalid")


    #sets thread where state changer will be
    CommandLine.Start(posepipeline)


    
   
    t1 = threading.Thread(target=worker,args=( posepipeline,))
    t1.start()






    

    #if data['input']['type']=='ROS':
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print("shut")

    print("Exited Stuff")
    posepipeline.Stop()
    
    t1.join() 
    
    print("FINISHED ELEGANTLY")

    if data["model"]["record"]==True:
        recordeddata={
            "R":posepipeline.posescalculator.recordedRs,
            "T":posepipeline.posescalculator.recordedTs
        }

        FileIO.saveAsPickle("/recorded",recordeddata,posepipeline.folder,False,False)
    
    FileIO.saveAsPickle("/poses",{"R":posepipeline.posescalculator.R,"t":posepipeline.posescalculator.t},posepipeline.folder,False,False)
    
 

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