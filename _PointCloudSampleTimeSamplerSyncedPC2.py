#HERE WILL BE the v1, but organized in a good fashion
import ArucoInfoGetter
import rospy
import algos
import pickler as pickle
import message_filters

from sensor_msgs import point_cloud2

from sensor_msgs.msg import PointCloud2

import struct



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
    
    print(scene)
    camNames=IRos.getAllPluggedCameras()


    stateru = StateManager.State(len(camNames))

    commandline.Start(stateru,rospy)

    #fetch K of existing cameras on the files
    intrinsics = FileIO.getKDs(camNames)

    rospy.init_node('ora_ora_ora_ORAA', anonymous=True)

    pcer = PCGetter(camNames,intrinsics,stateru,scene)

    camSub=[]
    #getting subscirpters to use message fitlers on
    for name in camNames:
        camSub.append(message_filters.Subscriber("abretesesamo/depth_registered/points", PointCloud2))


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
        camNames.append(np.asarray(cam['name']))

    print("owow")
    print(t.shape)
    print("what is this")

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
            
            ola = point_cloud2.read_points_list(args[camId], skip_nans=True)
     
            x=[]
            y=[]
            z=[]
            r=[]
            g=[]
            b=[]
            for point in ola:
                x.append(point[0])
                y.append(point[1])
                z.append(point[2])

                rgb = point[3]

                ba = bytearray(struct.pack("f", rgb))  


                count = 0
                for bytte in ba:
                    if(count==0):
                        r.append(255-bytte)
                    if(count==1):
                        g.append(255-bytte)
                    if(count==2):
                        b.append(255-bytte)
                        
                    count=count+1
                   
            r=np.asarray(r)
            g=np.asarray(g)
            b=np.asarray(b)

            rgb = np.vstack([r,g,b])
            xyz = np.vstack([x,y,z])
            
            print(rgb.shape)

            print(xyz.shape)
            
            xyz= mmnip.Transform(xyz, self.scene[0][camId],self.scene[1][camId])
            

            pc = pointclouder.Points2Cloud(xyz.T,rgb.T)

            pcs.append(pc)

        self.state.pc = pointclouder.MergeClouds(pcs)

            


if __name__ == '__main__':
    main(sys.argv)