#HERE WILL BE the v1, but organized in a good fashion
import rospy
import message_filters

from sensor_msgs.msg import Image
import cv2
import open3d
import numpy as np
import time

import commandline

import StateManager

import json


from libs import *

import sys

import copy

def main(argv):
    
    
    freq=50
    print("FRAME RATE IS: " +str(freq))

    filename=""
    if(len(argv)>1):
        filename=argv[1]
    else:
        print("Scene File Needed")
        quit()

    #create save folder path
    myString=filename
    names = myString.split("/")
    myString = names[len(names)-1]
    myString = myString[0:myString.find(".")]

    scene = LoadScene(filename)
    scene=list(scene)

    camNames=scene[2]

    #confirm cameras are plugged in
    IRos.CheckCamArePluggedIn(camNames)


    stateru = StateManager.State(len(camNames),camPoses=scene,PCPath=myString)

    commandline.Start(stateru,rospy)

    #fetch K of existing cameras on the files
    intrinsics = FileIO.getKDs(camNames)

    rospy.init_node('ora_ora_ora_ORAA', anonymous=True)

    pcer = PCGetter(camNames,intrinsics,stateru,scene)

    camSub=[]
    #getting subscirpters to use message fitlers on
    for name in camNames:
        camSub.append(message_filters.Subscriber(name+"/rgb/image_color", Image))
        camSub.append(message_filters.Subscriber(name+"/depth_registered/image_raw", Image))


    ts = message_filters.ApproximateTimeSynchronizer(camSub,10, 1.0/freq, allow_headerless=True)
    ts.registerCallback(pcer.callback)
    print("callbacks registered")




    try:
        rospy.spin()
    except KeyboardInterrupt:
        print("shut")


def LoadJson(filename,mode="r"):
    f=open(filename,mode)
    scene = json.load(f)
    f.close()

    return scene

def LoadScene(filename):

    scene = LoadJson(filename)
    print("load scene")

    R=[]
    t=[]
    camNames=[]
    for cam in  scene['cameras']:
        R.append(np.asarray(cam['R'], dtype=np.float32))

        tt  =np.asarray(cam['t'], dtype=np.float32)
        if len(tt.shape)==1:
            tt = np.expand_dims(tt, axis=1)
        t.append(tt)

        camNames.append(cam['name'])


    

    return R,t,camNames

class PCGetter(object):

    def __init__(self,camNames,intrinsics,stateru,scene):
        print("initiated")

        self.camNames = camNames
        self.N_cams= len(camNames)

        self.state = stateru

        self.scene = scene

        #intrinsic Params
        self.intrinsics = intrinsics

    def callback(self,*args):

        #print("Callbacktime")

        pcs=[]
        pcs2=[]
        

        #iterate throguh cameras
        for camId in range(0,self.N_cams):
            

            #RGB
            rgb = IRos.rosImg2RGB(args[camId*2])
            #depth
            depth_reg = IRos.rosImg2Depth(args[camId*2+1])

            K = self.intrinsics['K'][self.camNames[camId]]

            #points,colors = mmnip.depthimg2xyz(depth_reg,rgb,self.intrinsics['K'][self.camNames[camId]])
            points = mmnip.depthimg2xyz2(depth_reg,K)
            points = points.reshape((480*640, 3))

            #print(points.shape)
            


            #print(colors.shape)
            rgb1 = rgb.reshape((480*640, 3))#colors
            
            pc = pointclouder.Points2Cloud(points,rgb1,clean=True)

            pcs.append(pc)
            pctemp =copy.deepcopy(pc)
            pctemp.transform(mmnip.Rt2Homo(self.scene[0][camId],self.scene[1][camId].T))
            pcs2.append(pctemp)

        self.state.pcs = pcs

        self.state.pc = pointclouder.MergeClouds(pcs2)

            


if __name__ == '__main__':
    main(sys.argv)