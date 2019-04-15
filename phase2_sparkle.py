#!/usr/bin/env python
# Software License Agreement (BSD License)
import numpy as np
import cv2
import pickler as pickle
import datetime
import aruco
import open3d
import Rtmat
import pprint


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
        self.Nmarkers = 12 #marker maximo + 1 markers must be contiguous for this to work
        self.markerIDoffset=-2

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
        
        #if more than one marker was detected
        if  ids is not None and len(ids)>1:

            #finds rotations and vectors and draws referential
            rots,tvecs,img = aruco.FindPoses(K,D,det_corners,hello,len(ids))

            #squeeze
            ids = ids.squeeze()

            
            for i in range(0,len(ids)):                
                for j in range(i+1,len(ids)):
                    #carefull with this line
                    obs={"from":(ids[i]+self.markerIDoffset),"to":(ids[j]+self.markerIDoffset),"rot":np.dot(rots[i],rots[j].T)}
                    observations.append(obs)


            B = problemDef(observations,self.Nmarkers)

            

            #calculates transpose
            self.C = self.C + np.dot(B.T,B)

        #shows video
        cv2.imshow("Image window", hello)
        cv2.waitKey(3)


def problemDef(observations,N):

    #creates the left matrix in the problem formulation
    Ident = np.zeros((len(observations)*3,N*3))


    #creates the right matrix in the problem formulatin
    A = np.zeros((len(observations)*3,N*3))
            
    cnt = 0
    for obs in observations:
        #fills the matrices according to the observed pairs
        Ident[cnt*3:cnt*3+3,obs['to']*3:obs['to']*3+3]= np.eye(3)
        A[cnt*3:cnt*3+3,obs['from']*3:obs['from']*3+3]= obs['rot'] # <- ESTE  .T NAO DEVIA AQUI ESTAR DE TODO MAS FAZ COM QUE FUNCIONE WRONG

        
        #print(obs)
        #print("Ident")
        #print(Ident[cnt*3:cnt*3+3,:])
        #print("A")
        #print(A[cnt*3:cnt*3+3,:])
        #raw_input("Press Enter to continue...")
        
        cnt=cnt+1
    return Ident - A

def TotalLeastSquares(C,Nleast,Nmarkers):
    '''
    ola
    '''


    u,s,vh = np.linalg.svd(C)
    

    print("u")
    print(u)
    #solution =np.concatenate((np.expand_dims(u[:,11],1),np.expand_dims(u[:,10],1), np.expand_dims(u[:,9],1)),1)
    solution = u[:,-Nleast:]
    print("sol")
    print(solution)
    
    #split in 3x3 matrices, dat are close to the rotation matrices but not quite
    rotsols = []
    solsplit = np.split(solution,Nmarkers)  

    #get actual rotation matrices by doing the procrustes
    for sol in solsplit:
        r,t=proc.procrustes(np.eye(3),sol)
        rotsols.append(r)

    return rotsols


def main():

    ig = InfoGetter()

    cameraName = "abretesesamo"

    rospy.init_node('my_name_is_jeff', anonymous=True)


    #fetch intrinsic parameters
    camInfo = rospy.wait_for_message("/"+cameraName + "/rgb/camera_info", CameraInfo)        

    rgb,depth = roscv.GetRGBD(cameraName)    
    #print(camInfo)
    K = np.asarray(camInfo.K).reshape((3,3))
    #print(K)
    #pickle.In("CameraInfo","K",K)
    #pickle.In("CameraInfo","dist",camInfo.D) 
    #subscribe
    rospy.Subscriber(cameraName+"/rgb/image_color", Image, ig.callback,(K,camInfo.D))


    try:
        rospy.spin()
    except KeyboardInterrupt:
        print("shut")

    cv2.destroyAllWindows()

    pickle.In("obs","AtA",ig.C)

    
    rotsols = TotalLeastSquares(ig.C,3,ig.Nmarkers)
    

    
    
    rref = rotsols[0].T

    frames =[]
    counter = 0
    #make ref 1 the reference and display rotations
    for r in rotsols:

        #r=np.dot(rref,r.T)
        refe = open3d.create_mesh_coordinate_frame(size = 0.6, origin = [0, 0, 0])

        trans = np.zeros((4,4))
        trans[3,3]=1
        trans[0,3]=counter #linha ,coluna
        trans[0:3,0:3]=r

        refe.transform(trans)
        frames.append(refe)

        counter = counter +1

    
    open3d.draw_geometries(frames)

    
    Rrel = Rtmat.genRotRel(rotsols)
    
    '''
    for i in range(0,ig.Nmarkers):
        for j in range(0,ig.Nmarkers):
            print("Ok:",(i,j))
            print(Rrelations[j][i])
    '''

    pickle.In("obs","RelMarkerRotations",Rrelations)
     

if __name__ == '__main__':
    main()
