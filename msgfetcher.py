#!/usr/bin/env python

from sensor_msgs.msg import Image
from sensor_msgs.msg import CameraInfo
from sensor_msgs.msg import PointCloud2
import rospy
import numpy as np
import cv2
from cv_bridge import CvBridge
from matplotlib import pyplot as plt
import open3d
import converter

import scipy


def main():



    rgb = {}
    rgbline = {}
    depth = {}
    kp = {}
    des = {}
    XYZ = {}
    PClouds = {}

    cameraNames=["abretesesamo","ervilhamigalhas"]

    #bridge to convert ROS image into numpy array
    br = CvBridge()

    #fetches K of rgb cam - shouldnt it be DEPTH?????????????? - ros doenst give it
    topicRGBInfo = "/rgb/camera_info"
    rospy.init_node('my_name_is_jeff', anonymous=True)
    camInfo = rospy.wait_for_message("/ervilhamigalhas/rgb/camera_info", CameraInfo)

    #camera 0 ==

    #fetches ROS Rgb and depth image
    rgbros,depthros = FetchDepthRegisteredRGB(cameraNames[0])

    #converts ros img to numpy array
    rgb[cameraNames[0]] = br.imgmsg_to_cv2(rgbros, desired_encoding="passthrough")
    depth[cameraNames[0]] = br.imgmsg_to_cv2(depthros, desired_encoding="passthrough")
      
    #camera 1 ==

    #fetches ROS Rgb and depth image
    rgbros,depthros = FetchDepthRegisteredRGB(cameraNames[1])
    
    #converts ros img to numpy array
    rgb[cameraNames[1]] = br.imgmsg_to_cv2(rgbros, desired_encoding="passthrough")
    depth[cameraNames[1]] = br.imgmsg_to_cv2(depthros, desired_encoding="passthrough")



    #convert depth image to 3D vector
    for name in cameraNames:

        #fetches kps and descriptors of camera 1
        kp[name], des[name]  = SIFTer(rgb,name)

        #converts into 3d points
        XYZ[name] = depthimg2xyz(depth[name],camInfo.K)

        #reshape - straighten vectors
        XYZ[name] = XYZ[name].reshape(640*480,-1)
        rgbline[name] = rgb[name].reshape(640*480,-1)
            
        #make point cloud    
        PClouds[name] = open3d.PointCloud()
        PClouds[name].points = open3d.Vector3dVector(XYZ)
        PClouds[name].colors = open3d.Vector3dVector(rgbline/256.0) #range is 0-1 hence the division
   

    #initializes bruteforce matcher 
    bf = cv2.BFMatcher()

    #finds 2 nearest results(k=2)
    matches = bf.knnMatch( des[cameraNames[0]], des[cameraNames[1]], k=2)
    
    print("Transformation Done")

    # Apply ratio test
    good = []
    
    differenceRatio = 0.75  #is supposed to be around 0.25

    #only works for k=2 ( m,n are 2 variables)
    for m,n in matches:

        #se a distancia entre os descritores mais proximos e os segundos mais proximo for grande o suficiente (25% menor)
        if m.distance < (1-differenceRatio)*n.distance:
            good.append(m) #was  good.append([m]) 1.0


    #queryIdx - The index or row of the kp1 interest point matrix that matches
    #trainIdx - The index or row of the kp2 interest point matrix that matches
    
    #RANSAC Loop

    #only works for 2 cameras starting here


    #fetch 4 points from each camera

    #Procrustes

    #x ,y = kp1[500].pt
    #print(x,y)
    x=int(round(x))
    y=int(round(y)) #just doing int would floor instead of round

   
    # cv2.drawMatchesKnn expects list of lists as matches.
    #img3 = cv2.drawMatches(cv_rgb1,kp1,cv_rgb2,kp2,good,None,flags=2) #was drawMatchesKnn 1.0
    
            

 

    
    #fig = plt.figure()
    #plt.imshow(img3)
    #plt.show()
    #plt.draw()
    #plt.pause(2) # <-------
    #raw_input("<Hit Enter To Close>")
    #plt.close(fig)
    
def depthimg2xyz(depthimg,K):

    fx=K[0]
    fy=K[4]
    cx=K[2]
    cy=K[5]
    
    print(fx,fy)

    depthcoords = np.zeros((480, 640,3)) #height by width  by 3(X,Y,Z)

    u,v =np.indices((480,640))
    
    u=u-cx
    v=v-cy

    depthcoords[:,:,2]= depthimg/1000.0
    depthcoords[:,:,0]= depthcoords[:,:,2]*v/fx
    depthcoords[:,:,1]= depthcoords[:,:,2]*u/fy

    return depthcoords

def SIFTer(img,name="bigchungus",debug=False):


    

        
    if debug==True :
        cv2.imshow('image',img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    gray= cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    if debug==True :
        cv2.imshow('image',gray)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    sift= cv2.xfeatures2d.SIFT_create()
    #sift = cv2.SIFT()

    #kp = sift.detect(gray,None)
    kp, des = sift.detectAndCompute(gray,None)

    img2 = cv2.drawKeypoints(gray,kp,None)
    cv2.imwrite(name+".jpg",img2)

    return kp,des


def FetchDepthRegisteredRGB(cameraName):
    rospy.init_node('my_name_is_jeff', anonymous=True)

    topicRGB = "/rgb/image_color"
    topicDepth ="/depth_registered/image_raw"


    rgb = rospy.wait_for_message(cameraName + topicRGB, Image)
    depth_registered = rospy.wait_for_message(cameraName + topicDepth, Image)
    
    return rgb,depth_registered





if __name__ == '__main__':
    main()