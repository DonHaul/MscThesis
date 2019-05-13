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
    
    print(R,t,camNames)
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

    try:
        while True:
            #get clouds here
            pcs_frame=[]
            for i in range(0,len(camsName)):

                print("hello1")
                pc,rgb,depth = rosinterface.GetPointCloudRGBD(camsName[i],globalthings.camInfo['K'])
                print("hello2")
                points =  np.asarray(pc.points)

                #print(points.shape)
                print("hello3")
                pointsvs= mmnip.Transform(points.T,R[i],t[i])
                #rotation and translation is done here
                print(pc)
                print("hello4")
                pc.points = open3d.Vector3dVector(pointsvs.T)

                
                print("hello4")
                pcs_frame.append(pc)

                print("hello5")
            fullPc = pointclouder.MergeClouds(pcs_frame)
            
            print("hello6")
            refe = open3d.create_mesh_coordinate_frame(1, origin = [0, 0, 0])

            visu.draw_geometry([fullPc,refe])
            #if save_image:
            # vis.capture_screen_image("temp_%04d.jpg" % i)

            #time.sleep(1)
    except KeyboardInterrupt:
        print('interrupted!')
    

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

        print("Callbacktime")

        pcs=[]
        

                #iterate throguh cameras
        for camId in range(0,self.N_cams):
            

            #RGB
            rgb = IRos.rosImg2RGB(args[camId*2])
            #depth
            depth_reg = IRos.rosImg2Depth(args[camId*2+1])

            points = mmnip.depthimg2xyz(depth_reg,self.intrinsics['K'][self.camNames[camId]])
            points = points.reshape((480*640, 3))



            rgb1 = rgb.reshape((480*640, 3))

            pc = pointclouder.Points2Cloud(points,rgb1)

            points =  np.asarray(pc.points)

            pointsvs= mmnip.Transform(points.T, self.scene[i]['R'],self.scene[i]['t'])
            #rotation and translation is done here
            #print(pc)
            #print("hello4")
            pc.points = open3d.Vector3dVector(pointsvs.T)


            pcs.append(pc)

        self.state.pc = pointclouder.MergeClouds(pcs)

            


if __name__ == '__main__':
    main(sys.argv)