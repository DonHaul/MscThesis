#!/usr/bin/env python
# Software License Agreement (BSD License)
import numpy as np
import cv2
import pickler as pickle
import datetime
import aruco
import math


## Simple talker demo that listens to std_msgs/Strings published 
## to the 'chatter' topic

import rospy
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import CameraInfo
from sensor_msgs.msg import Image
import rosinterface as roscv
import visu
import procrustes as proc
import time



class InfoGetter(object):
    def __init__(self):
      
        self.count = 0
        self.Nmarkers = 14 #marker maximo + 1

        self.C = np.zeros((self.Nmarkers *3,self.Nmarkers *3))

        


    def callback(self,data,args):

        K=args[0]
        D=args[1]
        
        self.count = self.count +1

        #print(time.time())
        #rospy.loginfo(rospy.get_caller_id() + 'I heard it')
        img = roscv.rosImg2RGB(data)
        
        det_corners, ids, rejected = aruco.FindMarkers(img, K)

        hello = img.astype(np.uint8).copy() 
        hello = cv2.aruco.drawDetectedMarkers(hello,det_corners,ids)

        

        observations = []
        
        if  ids is not None and len(ids)>1:


            rots,tvecs,img = aruco.FindPoses(K,D,det_corners,hello,len(ids))

            ids = ids.squeeze()

            
            for i in range(0,len(ids)):                
                for j in range(i+1,len(ids)):
                    obs={"from":ids[i],"to":ids[j],"rot":np.dot(rots[i],rots[j].T)}
                    observations.append(obs)

            #creates the left matrix in the problem formulation
            Ident = np.zeros((len(observations)*3,self.Nmarkers*3))

            #creates the right matrix in the problem formulatin
            A = np.zeros((len(observations)*3,self.Nmarkers*3))
                    
            cnt = 0
            for obs in observations:
                #print(obs)
                Ident[cnt*3:cnt*3+3,obs['to']*3:obs['to']*3+3]= np.eye(3)
                A[cnt*3:cnt*3+3,obs['from']*3:obs['from']*3+3]= obs['rot']

                cnt=cnt+1
                
            B = Ident - A

            self.C = self.C + np.dot(B.T,B)

            #pickle.In("obs",ig.C)


        
        

        #print(self.count)
        #print(observations)
        #if(len(observations)>0):
        #    print(np.dot( rots[observations[0]['to']],rots[observations[0]['from']].T) )
        cv2.imshow("Image window", hello)
        cv2.waitKey(3)

# Checks if a matrix is a valid rotation matrix.
def isRotationMatrix(R) :
    Rt = np.transpose(R)
    shouldBeIdentity = np.dot(Rt, R)
    I = np.identity(3, dtype = R.dtype)
    n = np.linalg.norm(I - shouldBeIdentity)
    return n < 1e-6
 
 
# Calculates rotation matrix to euler angles
# The result is the same as MATLAB except the order
# of the euler angles ( x and z are swapped ).
def rotationMatrixToEulerAngles(R) :
 
    assert(isRotationMatrix(R))
     
    sy = math.sqrt(R[0,0] * R[0,0] +  R[1,0] * R[1,0])
     
    singular = sy < 1e-6
 
    if  not singular :
        x = math.atan2(R[2,1] , R[2,2])
        y = math.atan2(-R[2,0], sy)
        z = math.atan2(R[1,0], R[0,0])
    else :
        x = math.atan2(-R[1,2], R[1,1])
        y = math.atan2(-R[2,0], sy)
        z = 0
 
    return np.array([x, y, z])

    

def main():

    global count
    count = 0
    datdata={}

    ig = InfoGetter()

    cameraName = "abretesesamo"
    rgb=0

    rospy.init_node('my_name_is_jeff', anonymous=True)
    camInfo = rospy.wait_for_message("/"+cameraName + "/rgb/camera_info", CameraInfo)
        
    rgb,depth = roscv.GetRGBD(cameraName)
    
    K = np.asarray(camInfo.K).reshape((3,3))

    #det_corners, ids, rejected = aruco.FindMarkers(rgb, K)

    #hello = rgb.astype(np.uint8).copy() 
    #hello = cv2.aruco.drawDetectedMarkers(hello,det_corners,ids)

    #rots,tvecs,img = aruco.FindPoses(K,camInfo.D,det_corners,hello,len(ids))
   
    #visu.plotImg(img)

    rospy.Subscriber(cameraName+"/rgb/image_color", Image, ig.callback,(K,camInfo.D))

    # spin() simply keeps python from exiting until this node is stopped
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print("shut")

    cv2.destroyAllWindows()

        
    
    #pickle.In("AtA",ig.C)

    print("No more observations being fetched.")
    #print(ig.C)


    u, s, vh = np.linalg.svd(ig.C)
    #print("Eigenfs")
    #print(u.shape, s.shape, vh.shape)

    solution = u[:,-3:]

    rotsols = []
    solsplit = np.split(solution,ig.Nmarkers)

    for sol in solsplit:
        r,t=proc.procrustes(np.eye(3),sol)
        rotsols.append(r)
    
    for r in rotsols:
        angs = rotationMatrixToEulerAngles(r)
        print(angs)




if __name__ == '__main__':
    main()
