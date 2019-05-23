import sys,getopt
import rospy
from optparse import OptionParser
import json
import rosinterface
import numpy as np

import datetime

import pickler2 as pickle

import message_filters

from sensor_msgs.msg import Image
import random

import CamPoseGetter


import algos
import cv2

import FileIO

import matmanip as mmnip

import commandline

import StateManager

import visu

import libs.errorCalcs as errorCalcs
import libs.helperfuncs as helperfuncs

import matplotlib.pyplot as plt

def main(argv):
    #modes 
    #realtime
    #snap
    #oneforall

    freq=50

    arucoData, arucoModel,settings,camNames = ParsingInputs(argv)

    if camNames is None:
        camNames = rosinterface.getAllPluggedCameras()

    
    print(camNames)
    

    #fetch K of existing cameras on the files
    intrinsics = FileIO.getKDs(camNames)

    #has all states that may change
    stateru = StateManager.State(len(camNames),"realtime")

    

    rospy.init_node('do_u_kno_di_wae', anonymous=True)

    #Load aruco Model
    arucoModel = FileIO.getJsonFromFile("./scenes/falcon 23-05-2019 03:02:21.json")

    #sets class where image thread will run
    camposegetter=CamPoseGetter.CamPoseGetter(camNames,arucoData,arucoModel,intrinsics,stateru)



    #sets thread where state changer will be
    commandline.Start(stateru,rospy)

    camSub = []

    #getting subscirpters to use message fitlers on
    for name in camNames:
        camSub.append(message_filters.Subscriber(name+"/rgb/image_color", Image))

    ts = message_filters.ApproximateTimeSynchronizer(camSub,20, 1.0/freq, allow_headerless=True)
    ts.registerCallback(camposegetter.callback)

    print("Fetching Messages")    
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print("shut")


    cv2.destroyAllWindows()

    print("Finished Elegantly")


    if(type(stateru.t)!=list):
        print("the ol' reliable")
        stateru.t = [stateru.t,np.zeros(3,)]
        stateru.R = [stateru.R.T,np.eye(3)]

    visu.ViewRefs(stateru.R,stateru.t,refSize=1,showRef=True)

    
    print(type(stateru.t))
    visu.ViewRefs(stateru.R,stateru.t,refSize=0.1,showRef=True)


    print("R is:")
    print(stateru.R)

    print("t is:")
    print(stateru.t)

    if stateru.data['errorCalc']==True:

        LL =  helperfuncs.replicateThingInList(stateru.R,len(stateru.data['Rs']))
        print(len(LL))
        print(LL[0].shape)
        print(stateru.data['Rs'][0])

        y,x = errorCalcs.MatrixListError(stateru.data['Rs'],LL)

        plt.plot(x,y)
        plt.ylabel('some numbers')
        plt.show()


    SaveCameraPoses(stateru.R,stateru.t,camNames,"cameras")

def SaveCameraPoses(R,t,camNames,objectname="cameras"):


    f=open("static/names.json","r")

    arr = json.load(f)

    filename = random.choice(arr)
    f.close()

    fullfile={}
    fullfile[objectname]=[]

    for RR,tt,cc in zip(R,t,camNames):
        fullfile[objectname].append({"R":RR.tolist(),"t":tt.tolist(),"name":cc})

    saveName = filename+" " +  datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    f = open("./scenes/"+saveName+".json","w")



    json.dump(fullfile,f)
    
    f.close()

    print("Saved File: "+str(saveName))





def ParsingInputs(argv):
    parser = OptionParser()
    parser.add_option("-a", "--aruco")
    parser.add_option("-m", "--arucomodel")
    parser.add_option("-s", "--settings")
    parser.add_option("-c", "--cameras",action="append")

    (options, args) = parser.parse_args()

    #for opt in options:
    #    print(opt)
    print(options)
    f=None
    options = options.__dict__
    #aruco data

    if options['aruco'] is not None:
        f=open(options['aruco'],"r")
    else:
        f=open("./static/ArucoWand.json","r")
    
    arucoData = json.load(f)

    f.close()

    #settings

    if options['settings'] is not None:
        f=open(options['settings'],"r")
    else:
        f=open("./static/obsconfig_default.json","r")
    
    settings = json.load(f)

    f.close()

    #aruco model

    if options['arucomodel'] is not None:
        f=open(options['arucomodel'],"r")
    else:
        print("CREATE DEFAULT ARUCO MODEL")#f=open("./static/obsconfig_default.json","r")
    
    print("not loading model right now")
    #arucoModel = json.load(f)
    arucoModel = None

    f.close()    

    #cameras
    #print(options['cameras'])

    return arucoData , arucoModel,settings,options['cameras']

if __name__ == '__main__':
    main(sys.argv[1:])