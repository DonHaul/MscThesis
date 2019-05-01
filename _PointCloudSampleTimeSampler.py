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

def main():
    

    camsName=["abretesesamo","ervilhamigalhas"]

    print(sys.argv)

    camPoses= pickle.Pickle().Out("static/CamPose_NEW2camAruco_4 01-05-2019 16-55-43.pickle")
    

    R= camPoses['R']
    print(R)
    tt= camPoses['t']
    
    t=[]
    for t2 in tt:
        t.append(t2-tt[0])
        
    print(t)

    t[1]= np.array([[-0.72],[0],[0.58]])
    #print(a)

    visu.ViewRefs(R)
    

    pcl =[]#list in time

    try:
        while True:
            #get clouds here
            pcs_frame=[]
            for i in range(0,len(camsName)):

    
                pc,rgb,depth = rosinterface.GetPointCloudRGBD(camsName[i],globalthings.camInfo['K'])

                points =  np.asarray(pc.points)

                print(points.shape)

                pointsvs= mmnip.Transform(points.T,R[i].T,mmnip.InvertT(R[i],t[i]) )
                #rotation and translation is done here
                print(pc)

                pc.points = open3d.Vector3dVector(pointsvs.T)



                pcs_frame.append(pc)

            fullPc = pointclouder.MergeClouds(pcs_frame)
                
            refe = open3d.create_mesh_coordinate_frame(1, origin = [0, 0, 0])

            visu.draw_geometry([fullPc,refe])
            #if save_image:
            # vis.capture_screen_image("temp_%04d.jpg" % i)

            #time.sleep(1)
    except KeyboardInterrupt:
        print('interrupted!')
    

    #vis.destroy_window()

   


if __name__ == '__main__':
    main()