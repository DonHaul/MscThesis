#!/usr/bin/env python

from sensor_msgs.msg import Image
import rospy
import cv2
from cv_bridge import CvBridge
from matplotlib import pyplot as plt

def main():

    br = CvBridge()

    #make the message fetch syncrhonous, it inst right now
    rgb,depth = FetchDepthRegisteredRGB("/abretesesamo")

    
    cv_rgb1 = br.imgmsg_to_cv2(rgb, desired_encoding="passthrough")
    cv_depth = br.imgmsg_to_cv2(depth, desired_encoding="passthrough")

    kp1,des1 = SIFTer(cv_rgb1,"abretesesamo")

    #make the message fetch syncrhonous, it inst right now
    rgb,depth = FetchDepthRegisteredRGB("/ervilhamigalhas")
    
    
    cv_rgb2 = br.imgmsg_to_cv2(rgb, desired_encoding="passthrough")
    cv_depth = br.imgmsg_to_cv2(depth, desired_encoding="passthrough")

    kp2,des2 = SIFTer(cv_rgb2,"ervilhamigalhas")

    bf = cv2.BFMatcher()
    matches = bf.knnMatch(des1,des2, k=2)

    # Apply ratio test
    good = []

    print(len(matches))
    count=0

    #only works for k=2 ( m,n are 2 variables)
    for m,n in matches:

        #se a distancia entre os descritores mais proximos e os segundos mais proximo for grande o suficiente (25% menor)
        if m.distance < 0.75*n.distance:
            good.append(m) #was  good.append([m]) 1.0

    print(good)
    #for m  in good:
    #    print(m.distance)

    
    # cv2.drawMatchesKnn expects list of lists as matches.
    img3 = cv2.drawMatchesKnn(cv_rgb1,kp1,cv_rgb2,kp2,good,None,flags=2) #was drawMatchesKnn 1.0
        


    plt.imshow(img3),plt.show()
    

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