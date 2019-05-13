#HERE WILL BE the v1, but organized in a good fashion
import ArucoInfoGetter
import rospy
import algos
import pickler as pickle
from sensor_msgs.msg import Image

import cv2
import open3d
import numpy as np
import visu
import matmanip as mmnip
import time
import rosinterface
import pointclouder
import globalthings


import pickler2 as pickle

import sys

def main(argv):
    
    
    camsName=["abretesesamo","ervilhamigalhas"]

    print(sys.argv)

    camPoses= pickle.Pickle().Out("pickles/CamPose_NEW2camAruco_4 02-05-2019 14-09-42.pickle")
    

    R= camPoses['R']
    print(R)
    t= camPoses['t']


    #t[0] = mmnip.InvertT(R[0],t[0])
    #R[0]=R[0].T
    #t[0] = mmnip.InvertT(R[0],t[0])
    #t[1] = mmnip.InvertT(R[1],t[1])
    #R[1]=R[1].T

    #t[2] = mmnip.InvertT(R[2],t[2])
    #R[2]=R[2].T
    #t=[]
    #for t2 in tt:
    #    t.append(t2-tt[0])
        
    print(t)

    #t[1]= np.array([[-0.72],[0],[0.58]])
    #print(a)

    visu.ViewRefs(R,t,refSize=0.1)
    

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

   


if __name__ == '__main__':
    main(sys.argv[1:])