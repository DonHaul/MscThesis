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

def main():
    from globalthings import *

    camsName=["abretesesamo","ervilhamigalhas"]



    pcl =[]#list in time

    try:
        while True:
            #get clouds here
            pcs_frame=[]
            for i in range(0,len(camsName)):

    
                pc,rgb,depth = rosinterface.GetPointCloudRGBD(camsName[i],camInfo['K'])

                pcs_frame.append(pc)
                #rotation and translation is done here

            fullPc = pointclouder.MergeClouds(pcs_frame)
                
            

            visu.draw_geometry([fullPc])
            #if save_image:
            # vis.capture_screen_image("temp_%04d.jpg" % i)

            #time.sleep(1)
    except KeyboardInterrupt:
        print('interrupted!')
    

    vis.destroy_window()

   


if __name__ == '__main__':
    main()