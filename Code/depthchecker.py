#HERE WILL BE the v1, but organized in a good fashion
import rospy
import message_filters
from sensor_msgs.msg import Image
from sensor_msgs.msg import PointCloud2
from sensor_msgs import point_cloud2

import struct

import cv2
import open3d
import numpy as np
import time
from sensor_msgs.msg import CameraInfo


import sys

from libs import *

def main(argv):
    

    
    freq=1

    camNames = IRos.getAllPluggedCameras()
    camName = "camera"

    
    #fetch K of existing cameras on the files
    intrinsics = FileIO.getIntrinsics(['speedwagon'])

    rospy.init_node('ora_ora_ora_ORAA', anonymous=True)


    #initializes class
    pcer = PCGetter(camName,intrinsics)
    print(camName)
    camSub=[]
    #getting subscirpters to use message fitlers on
    camSub.append(message_filters.Subscriber(camName+"/rgb/image_raw", Image))
    camSub.append(message_filters.Subscriber(camName+"/depth/image_raw", Image))
    camSub.append(message_filters.Subscriber(camName+"/depth_registered/points", PointCloud2))
    #camSub.append(message_filters.Subscriber(camName+"/depth/points", PointCloud2))


    ts = message_filters.ApproximateTimeSynchronizer(camSub,1, 1.0/freq, allow_headerless=True)
    ts.registerCallback(pcer.callback)
    print("callbacks registered")




    try:
        rospy.spin()
    except KeyboardInterrupt:
        print("shut")


    print("FINISHED")


class PCGetter(object):

    def __init__(self,camName,intrinsics):
        print("initiated")

        self.camName = camName
        
        #intrinsic Params
        self.intrinsics = intrinsics


    def callback(self,*args):

        print("HHEYGWY")
       

        rgb = IRos.rosImg2RGB(args[0])
        depth_reg = IRos.rosImg2Depth(args[1])


        #copy image
        hello = rgb.astype(np.uint8).copy() 

        cv2.imshow("wow",hello)
        cv2.waitKey(1000)
        cv2.destroyAllWindows()


        points = mmnip.depthimg2xyz2(depth_reg,self.intrinsics['speedwagon']['depth']['K'],(360,480))
        print(points.shape)
        points = points.reshape((360*480, 3))
        print(points.shape)

        rgbd = mmnip.xyz2rgbd(points, rgb, self.intrinsics['speedwagon']['depth']['R'] , self.intrinsics['speedwagon']['depth']['P'][:,3] , self.intrinsics['speedwagon']['rgb']['K'])

        cv2.imshow("wow",rgbd)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        print("HOLA")
        print(rgbd.shape)
        rgbd=cv2.resize(rgbd,(480,360))
        print(rgbd.shape)
        cv2.imshow("wow",rgbd)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        rgb1=rgbd.reshape((360*480, 3))

        pc1 = pointclouder.Points2Cloud(points,rgb1)

        open3d.draw_geometries([pc1])

        
        #get matrix intrinsics
        #K = self.intrinsics[]['K'][self.camName]
        #D = self.intrinsics['D'][self.camName]





        pc = point_cloud2.read_points_list( args[2], skip_nans=True)

        print("pc len")
        print(len(pc))

        x=[]
        y=[]
        z=[]
        r=[]
        g=[]
        b=[]
        for point in pc:

            print(point)

            x.append(point[0])
            y.append(point[1])
            z.append(point[2])


        xyz = np.vstack([x,y,z])
        

        pc = pointclouder.Points2Cloud(xyz.T)

        visu.draw_geometry([pc,pc1])

        

            


if __name__ == '__main__':
    main(sys.argv)