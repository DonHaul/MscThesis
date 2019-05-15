#HERE WILL BE the v1, but organized in a good fashion
import ArucoInfoGetter
import rospy
import algos
import pickler as pickle
import message_filters

from sensor_msgs.msg import Image
import cv2
import open3d
import numpy as np
import visu
import matmanip as mmnip
import time
import rosinterface as IRos
import pointclouder

import commandline

import StateManager

import json

import open3d

import pickler2 as pickle

import FileIO

import sys


def main(argv):
    
    freq=10

    filename=""
    if(len(argv)>1):
        filename=argv[1]
    else:
        print("Scene File Needed")
        quit()
        
    #R,t,camNames
    scene = LoadScene(filename)
    scene=list(scene)
    mmnip.isRotation(scene[0])
 
    scene[0]=mmnip.genRotRelLeft(scene[0])
    
    visu.ViewRefs(scene[0],scene[1],refSize=0.1)

    print(scene[0])
    camNames=scene[2]#IRos.getAllPluggedCameras()
    print(camNames)
    #quit()

    stateru = StateManager.State(len(camNames))

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



    pcl =[]#list in time

    open3d.write_point_cloud("./tmp/wow.ply", stateru.pc)

    #vis.destroy_window()

def LoadJson(filename,mode="r"):
    f=open(filename,mode)
    scene = json.load(f)
    f.close()

    return scene

def LoadScene(filename):

    scene = LoadJson(filename)


    R=[]
    t=[]
    camNames=[]
    for cam in  scene['cameras']:
        R.append(np.asarray(cam['R'], dtype=np.float32))
        t.append(np.asarray(cam['t'], dtype=np.float32))
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

            print(points.shape)
            points= mmnip.Transform(points.T, self.scene[0][camId], self.scene[1][camId]).T


            #print(colors.shape)
            rgb1 = rgb.reshape((480*640, 3))#colors
            
            pc = pointclouder.Points2Cloud(points,rgb1)

            #points =  np.asarray(pc.points)

            #print(points,shape)

            
            #rotation and translation is done here
            #print(pc)
            #print("hello4")
            #pc.points = open3d.Vector3dVector(pointsvs)


            pcs.append(pc)

        self.state.pc = pointclouder.MergeClouds(pcs)

            


if __name__ == '__main__':
    main(sys.argv)