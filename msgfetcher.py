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
import procrustes as proc
import time

from scipy import spatial


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
        kp[name], des[name]  = SIFTer(rgb[name],name)

        #converts into 3d points
        XYZ[name] = depthimg2xyz(depth[name],camInfo.K)
        
        #reshape - straighten vectors
        XYZ[name] = XYZ[name].reshape(640*480,-1)
        rgbline[name] = rgb[name].reshape(640*480,-1)
            
        #make point cloud    
        PClouds[name] = open3d.PointCloud()
        PClouds[name].points = open3d.Vector3dVector(XYZ[name])
        PClouds[name].colors = open3d.Vector3dVector(rgbline[name]/256.0) #range is 0-1 hence the division
   

    #initializes bruteforce matcher 
    bf = cv2.BFMatcher()

    #finds 2 nearest results(k=2)
    matches = bf.knnMatch( des[cameraNames[0]], des[cameraNames[1]], k=2)
    
 

    #only works for 2 cameras starting here


    # Apply ratio test
    match1 = []
    match2 = []
    
    differenceRatio = 0.25  #is supposed to be around 0.25

    #only works for k=2 ( m,n are 2 variables)
    for m,n in matches:

        #se a distancia entre os descritores mais proximos e os segundos mais proximo for grande o suficiente (25% menor)
        if m.distance < (1-differenceRatio)*n.distance:
            match1.append(m.queryIdx) #was  good.append([m]) 1.0   was  good.append(m) 1.2
            match2.append(m.trainIdx)


    #queryIdx - The index or row of the kp1 interest point matrix that matches
    #trainIdx - The index or row of the kp2 interest point matrix that matches
    
    #this section is super slow make this matricial stuff

    goodkp1 = []

    #convert 2D map to array map
    for m in match1:
        x, y =  kp[cameraNames[0]][m].pt
        goodkp1.append(y*480+x)  #MIGHT NOT BE RIGHT

    
    goodkp2 = []
    #convert 2D map to array map
    for m in match2:
        x, y =  kp[cameraNames[1]][m].pt
        goodkp2.append(y*480+x) #MIGHT NOT BE RIGHT

    goodkp1 = np.rint(goodkp1)
    goodkp2 = np.rint(goodkp2)

    goodkp1 = goodkp1.astype(int)
    goodkp2 = goodkp2.astype(int)

    
    #apenas usa pontos emparelhados
    XYZ1 = XYZ[cameraNames[0]][goodkp1] #nmpy round to int
    XYZ2 = XYZ[cameraNames[1]][goodkp2] #nmpy round to int
    
    
    #inicializa highscore
    high_score_inliers = 0

    #RANSAC Loop

    

    #Procrustes
    perm = np.random.permutation(len(match1))
    perm = perm[0:4]


    #fetch 4  3D points from each camera
    P1 = XYZ1[perm,:]
    P2 = XYZ2[perm,:]

    _,_,proctf = proc.procrustes(P1,P2,scaling=False,reflection=False)            
    rot = proctf["rotation"]
    XYZ2in1=np.dot(XYZ2,rot.transpose())+   (np.ones([len(XYZ2),1])*proctf["translation"])
    
    
    temp = XYZ2in1 - XYZ1
    norms = np.linalg.norm(temp,axis=1)

    print(norms)
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