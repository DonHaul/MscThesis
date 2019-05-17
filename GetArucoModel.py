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

import ArucoInfoGetterv3 as arucoInfoGetter

import algos
import cv2

import FileIO

import matmanip as mmnip

import commandline

import StateManager

import FileIO


import visu

def main(argv):

    freq=50

    arucoData, arucoModel,settings,camNames = ParsingInputs(argv)

    if camNames is None:
        camNames = rosinterface.getAllPluggedCameras()

    #fetch K of existing cameras on the files
    intrinsics = FileIO.getKDs(camNames)

    #has all states that may change
    stateru = StateManager.State(len(arucoData['ids']))

    camName=camNames[0]
    

    rospy.init_node('do_u_kno_di_wae', anonymous=True)


    #sets class where image thread will run
    arucogetter=arucoInfoGetter.ArucoInfoGetterv3(camName,arucoData,intrinsics,stateru)

    #sets thread where state changer will be
    commandline.Start(stateru,rospy)


    rospy.Subscriber(camName+"/rgb/image_color", Image, arucogetter.callback)

    print("Fetching Messages")    
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print("shut")


    cv2.destroyAllWindows()

    print("Finished Elegantly")

    print("R is:")
    print(stateru.R)

    print("t is:")
    print(stateru.t)

    SaveCameraPoses(stateru.R,stateru.t,camName,nameofthing = "markers")

def SaveCameraPoses(R,t,camNames,nameofthing = "cameras"):


    f=open("static/names.json","r")

    arr = json.load(f)

    filename = random.choice(arr)
    f.close()

    fullfile={}
    fullfile[nameofthing]=[]

    for RR,tt,cc in zip(R,t,camNames):
        fullfile[nameofthing].append({"R":RR.tolist(),"t":tt.tolist(),"name":cc})

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