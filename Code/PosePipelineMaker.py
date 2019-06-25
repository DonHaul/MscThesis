"""
PosePipelineMaker.py

Generates and executes a pipeline to estimate poses
"""

import numpy as np
import time
import rospy
import numpy as np
from shutil import copyfile
from libs import *
import sys
import threading

#pipeline classes
from Classes.ImgReaders import RosStreamReader,ImgStreamReader,StreamReader
from Classes.ObservationGenners import CamerasObservationMaker,CangalhoObservationsMaker, CangalhoSynthObsMaker
from Classes.ArucoDetecc import CangalhoPnPDetector,CangalhoProcrustesDetector,SingleArucosDetector
from Classes.PosesCalculators import PosesCalculator, OutlierRemPoseCalculator , PosesCalculatorSynth
from Classes import PosePipeline

import CommandLine


def worker(posepipe):

    #executes pipeline untill it is stopped
    while True:
       
       #while there are new images
        if posepipe.imgStream.nextIsAvailable:

            #set input as consumed
            posepipe.imgStream.nextIsAvailable=False

            #gets next image
            streamData= posepipe.imgStream.next()

            #stop if there are no more images
            #if streamData is None:
            #    posepipe.Stop()
            #    break

            #generates observations
            img,ids,obsR,obsT = posepipe.ObservationMaker.GetObservations(streamData)

            #adds observations to matrices
            posepipe.posescalculator.AddObservations(obsR,obsT)
        else
            posepipe.Stop()
            break



        if posepipe.GetStop(): 
            break           
            



def main(argv):
   

    #Reads the configuration file
    data =  FileIO.getJsonFromFile(argv[0])
    

    posepipeline = PosePipeline.PosePipeline()

    #holds
    state={}

    posepipeline.folder = FileIO.CreateFolder("./PipelineLogs/"+FileIO.GetAnimalName())

    #saves pipeline configuration on the outputfolder
    FileIO.putFileWithJson(data,"pipeline",posepipeline.folder+"/")



    #hash of aruco detector classes
    arucodetectors={
        'singular':SingleArucosDetector.SingleArucosDetector,
        'allforone':CangalhoPnPDetector.CangalhoPnPDetector,
        'depthforone':CangalhoProcrustesDetector.CangalhoProcrustesDetector        }
    

    #Assigns the InputStream
    if data['input']['type']=='IMG':

        #must set path where images are
        posepipeline.imgStream = ImgStreamReader.ImgStreamReader(data['input']['path'])
    elif data['input']['type']=='ROS':

        camNames = []

        #sets cameras if there are any
        if "cameras" in data['model']:
            camNames = data['model']['cameras'] 

        
        posepipeline.imgStream = RosStreamReader.RosStreamReader(camNames=camNames)
    elif data['input']['type']=='SYNTH':
        posepipeline.imgStream = StreamReader.StreamReader()
        posepipeline.posescalculator=PosesCalculatorSynth.PosesCalculatorSynth()
    else:
        print("This Pipeline input is invalid")



    #setting stuff on state
    state['intrinsics'] = FileIO.getKDs(posepipeline.imgStream.camNames)
    state['arucodata'] = FileIO.getJsonFromFile(data['model']['arucodata'])
    state['arucomodel'] = FileIO.getFromPickle(data['model']['arucomodel'])


    #Assigns observation maker and posecalculator
    if data['model']['type']=='CANGALHO':
        

        #static parameters
        singlecamData={
            "K":state['intrinsics']['K'][imgStream.camNames[0]],
            "D":state['intrinsics']['D'][imgStream.camNames[0]],
            "arucodata":state['arucodata']}

        #sets observation maker
        posepipeline.ObservationMaker =  CangalhoObservationsMaker.CangalhoObservationMaker(singlecamData)

        #sets pose calculator
        posedata={
            "N_objects":len(state['arucodata']['ids']),
            "record":data["model"]["record"]
            }
        posepipeline.posescalculator = PosesCalculator.PosesCalculator(posedata)


    elif data['model']['type']=='CAMERA':

        #static parameters
        multicamData={
            "intrinsics":state['intrinsics'],
            "arucodata":state['arucodata'],
            "camnames":posepipeline.imgStream.camNames,
            "arucomodel":state['arucomodel'],
            "innerpipeline":{
                "arucodetector":arucodetectors[data['model']['arucodetection']]({'arucodata':state['arucodata'],'arucomodel':state['arucomodel']})
            }
            }
        
        #sets observation maker
        posepipeline.ObservationMaker = CamerasObservationMaker.CamerasObservationMaker(multicamData)

        #sets pose calculator
        posedata={
            "N_objects":len(posepipeline.imgStream.camNames),
            "record":data["model"]["record"]}
        

        #sets observation treatment
        if data['model']['mode']['type']=='REGULAR':
            posepipeline.posescalculator = PosesCalculator.PosesCalculator(posedata)
        
        elif data['model']['mode']['type']=='OUTLIERREMOVE':

            #static parameters
            posedata['observations']=data['model']['mode']['observations']
            posedata['Rcutoff']=data['model']['mode']['Rcutoff']
            posedata['Tcutoff']=data['model']['mode']['Tcutoff']

            posepipeline.posescalculator = OutlierRemPoseCalculator.OulierRemovalPoseCalculator(posedata)

        else:
            print("This pose calculator is invalid")

    elif data['model']['type']=='SYNTH_CANGALHO':
        posepipeline.ObservationMaker=
        
    else:
        print("This Pipeline Model is invalid")


    #sets thread for terminal window
    CommandLine.Start(posepipeline)

    #sets thread for pipeline
    t1 = threading.Thread(target=worker,args=( posepipeline,))
    t1.start()


    #spins ros if necessary
    if data['input']['type']=='ROS':
        try:
            rospy.spin()
        except KeyboardInterrupt:
            print("shut")

    print("Exited Stuff")
    posepipeline.Stop()
    
    t1.join() 
    
    print("FINISHED ELEGANTLY")

    #see and save resulting scene
    visu.ViewRefs(posepipeline.posescalculator.R,posepipeline.posescalculator.t,refSize=0.1,showRef=True,saveImg=True,saveName=posepipeline.folder+"/screenshot.jpg")
    
    #record r and t
    if data["model"]["record"]==True:
        recordeddata={
            "R":posepipeline.posescalculator.recordedRs,
            "T":posepipeline.posescalculator.recordedTs
        }

        print(len(recordeddata['R']))

        print(len(recordeddata['T']))

        FileIO.saveAsPickle("/recorded",recordeddata,posepipeline.folder,False,False)
    
    FileIO.saveAsPickle("/poses",{"R":posepipeline.posescalculator.R,"t":posepipeline.posescalculator.t},posepipeline.folder,False,False)
    
 

if __name__ == '__main__':
    main(sys.argv[1:])