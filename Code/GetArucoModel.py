import sys,getopt
import rospy
from optparse import OptionParser
import json
import numpy as np
import cv2
import datetime
import message_filters
from sensor_msgs.msg import Image
import random

import ArucoInfoGetterv3 as arucoInfoGetter

import commandline
import StateManager

from libs import *

def main(argv):

    freq=50

    arucoData, arucoModel,settings,camNames = ParsingInputs(argv)

    print(arucoData)


    if camNames is None:
        camNames = IRos.getAllPluggedCameras()

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

    if stateru.R is None or stateru.t is None:
        quit()


    newT = mmnip.Transl_fromWtoRef(stateru.R,stateru.t)

    filepath =  FileIO.saveAsPickle("ArucoModel",{'R':stateru.R,'T':newT},"arucoModels/")


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
        print("No Aruco Data File Specified: Using Defaul")
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