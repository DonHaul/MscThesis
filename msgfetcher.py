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

def main():

    cameraNames=["abretesesamo","ervilhamigalhas"]

    br = CvBridge()

    #make the message fetch syncrhonous, it inst right now
    rgb,depth = FetchDepthRegisteredRGB(cameraNames[0])

    
    cv_rgb1 = br.imgmsg_to_cv2(rgb, desired_encoding="passthrough")
    cv_depth1 = br.imgmsg_to_cv2(depth, desired_encoding="passthrough")

    cv_depth1 = np.array(cv_depth1)
    
    kp1,des1 = SIFTer(cv_rgb1,cameraNames[0])

    #make the message fetch syncrhonous, it inst right now
    rgb,depth = FetchDepthRegisteredRGB(cameraNames[1])
    
    
    cv_rgb2 = br.imgmsg_to_cv2(rgb, desired_encoding="passthrough")
    cv_depth2 = br.imgmsg_to_cv2(depth, desired_encoding="passthrough")

    cv_depth2 = np.array(cv_depth2)

    kp2,des2 = SIFTer(cv_rgb2,cameraNames[1])

    bf = cv2.BFMatcher()
    matches = bf.knnMatch(des1,des2, k=2)

    topicRGBInfo = "/rgb/camera_info"
    camInfo = rospy.wait_for_message("/ervilhamigalhas/rgb/camera_info", CameraInfo)
    

    xyz1 = depthimg2xyz(cv_depth1,camInfo.K)
    xyz2 = depthimg2xyz(cv_depth2,camInfo.K)
    
    xyz1 = xyz1.reshape(640*480,-1)

    print(xyz1.shape)

    pcd = open3d.PointCloud()
    pcd.points = open3d.Vector3dVector(xyz1)

    topicPC ="/depth_registered/points"   
    pcmsg = rospy.wait_for_message(cameraNames[0] + topicPC, PointCloud2)

    truecloud = converter.PC2toOpen3DPC(pcmsg)

    open3d.draw_geometries([truecloud,pcd])
    
    print("Transformation Done")

    # Apply ratio test
    good = []

    
    differenceRatio = 0.75  #is supposed to be around 0.25

    #only works for k=2 ( m,n are 2 variables)
    for m,n in matches:

        #se a distancia entre os descritores mais proximos e os segundos mais proximo for grande o suficiente (25% menor)
        if m.distance < (1-differenceRatio)*n.distance:
            good.append(m) #was  good.append([m]) 1.0

    #cv2.DMatch
    #queryIdx - The index or row of the kp1 interest point matrix that matches
    #trainIdx - The index or row of the kp2 interest point matrix that matches
    
    x ,y = kp1[500].pt
    print(x,y)
    x=int(round(x))
    y=int(round(y)) #just doing int would floor instead of round

    print(cv_depth1[x][y])
    
    # cv2.drawMatchesKnn expects list of lists as matches.
    img3 = cv2.drawMatches(cv_rgb1,kp1,cv_rgb2,kp2,good,None,flags=2) #was drawMatchesKnn 1.0
    
            

 

    
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
    print(fx,fy)

    depthcoords = np.zeros((480, 640,3)) #height by width  by 3(X,Y,Z)

    u,v =np.indices((480,640))

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