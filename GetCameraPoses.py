import sys,getopt
import rospy
from optparse import OptionParser
import json
import rosinterface
import numpy as np

import datetime

import pickler2 as pickle

import message_filters

import random

import CamPoseGetter

from sensor_msgs.msg import Image

import algos
import cv2

import matmanip as mmnip

import commandline

import StateManager

import visu

def main(argv):

    freq=50

    arucoData, arucoModel,settings,camNames = ParsingInputs(argv)

    if camNames is None:
        camNames = rosinterface.getAllPluggedCameras()

    #fetch K of existing cameras on the files
    intrinsics = getKDs(camNames)

    #has all states that may change
    stateru = StateManager.State(len(camNames))



    rospy.init_node('do_u_kno_di_wae', anonymous=True)

    #Load aruco Model
    arucoModel = pickle.Pickle().Out("static/ArucoModel 01-05-2019 15-38-20.pickle")

    #sets class where image thread will run
    camposegetter=CamPoseGetter.CamPoseGetter(camNames,arucoData,arucoModel,intrinsics,stateru)

    #sets thread where state changer will be
    commandline.Start(stateru,rospy)

    camSub = []

    #getting subscirpters to use message fitlers on
    for name in camNames:
        camSub.append(message_filters.Subscriber(name+"/rgb/image_color", Image))

    ts = message_filters.ApproximateTimeSynchronizer(camSub,10, 1.0/freq, allow_headerless=True)
    ts.registerCallback(camposegetter.callback)

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

    SaveCameraPoses(stateru.R,stateru.t)

def SaveCameraPoses(R=[],t=[]):


    f=open("static/names.json","r")

    arr = json.load(f)

    filename = random.choice(arr)
    f.close()

    fullfile={}
    fullfile["cameras"]=[]

    for RR,tt in zip(R,t):
        ["cameras"].append({"R":RR.tolist(),"t":tt.tolist()})

    saveName = filename+" " +  datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    f = open("./scenes/"+saveName+".json","w")

    json.dump(fullfile,f)
    
    f.close()

def getKDs(camNames):
    K={}
    D={}

    for name in camNames:
        filedict = getJsonFromFile("./static/camcalib_" + name +".json")

        #if file does not exist
        if(filedict==None):
            filedict = getJsonFromFile("./static/camcalib_default.json")

        k = np.asarray(filedict['K'], dtype=np.float32)

        
        K[name]=k
        D[name]=np.asarray(filedict['D'], dtype=np.float32)

        intrinsic = {"K":K,"D":D}

    return intrinsic

def getJsonFromFile(filename):

    try:
        f=open(filename,"r")
    
        data = json.load(f)
        f.close()

        return data

    except IOError:
      print "Error: File does not appear to exist."
      return None



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