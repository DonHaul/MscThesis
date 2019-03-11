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
import scipy.io as sio

from scipy import spatial
#mat_contents = sio.loadmat('octave_a.mat')

def main():



    rgb = {}
    rgbline = {}
    depth = {}
    kp = {}
    des = {}
    XYZ = {}
    XYZline = {}
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

    #plotImg(rgb[cameraNames[1]] )


    
    
    depth[cameraNames[1]] = br.imgmsg_to_cv2(depthros, desired_encoding="passthrough")

   

    #convert depth image to 3D vector
    for name in cameraNames:

        #fetches kps and descriptors of camera 1
        kp[name], des[name]  = SIFTer(rgb[name],name)

        #converts into 3d points
        XYZ[name] = depthimg2xyz(depth[name],camInfo.K)
        
        #reshape - straighten vectors
        XYZline[name] = XYZ[name].reshape(640*480,-1)
        rgbline[name] = rgb[name].reshape(640*480,-1)
            
        #make point cloud    
        PClouds[name] = open3d.PointCloud()
        PClouds[name].points = open3d.Vector3dVector(XYZline[name])
        PClouds[name].colors = open3d.Vector3dVector(rgbline[name]/256.0) #range is 0-1 hence the division
   

    #initializes bruteforce matcher 
    bf = cv2.BFMatcher()

    #finds 2 nearest results(k=2)
    matches = bf.knnMatch( des[cameraNames[0]], des[cameraNames[1]], k=2)
    
    draw_params = dict(matchColor = (0,255,0),
                   singlePointColor = (255,0,0),
                   flags = 0)
    
    #img3 = cv2.drawMatchesKnn(rgb[cameraNames[0]],kp[cameraNames[0]],rgb[cameraNames[1]],kp[cameraNames[1]],matches[:10],None,**draw_params)
    #plt.imshow(img3),plt.show()
    

    #only works for 2 cameras starting here


    # Apply ratio test
    match1 = []
    match2 = []

    goodmatch = []
    
    differenceRatio = 0.75  #is supposed to be around 0.25

    #only works for k=2 ( m,n are 2 variables)
    for m,n in matches:

        #se a distancia entre os descritores mais proximos e os segundos mais proximo for grande o suficiente (25% menor)
        if m.distance < (1-differenceRatio)*n.distance:
            match1.append(m.queryIdx) #was  good.append([m]) 1.0   was  good.append(m) 1.2
            match2.append(m.trainIdx)

            goodmatch.append(m)

    img3 = cv2.drawMatches(rgb[cameraNames[0]],kp[cameraNames[0]],rgb[cameraNames[1]],kp[cameraNames[1]],goodmatch[:],None,**draw_params)

    plotImg(img3)
    



    #queryIdx - The index or row of the kp1 interest point matrix that matches
    #trainIdx - The index or row of the kp2 interest point matrix that matches
    
    #this section is super slow make this matricial stuff


    ## TODO: Checked UNTIL THIS LINE

    goodkp1 = []



    #convert 2D map to array map
    for m in match1:
        x, y =  kp[cameraNames[0]][m].pt

        x = Float2Int(x)
        y = Float2Int(y)

        goodkp1.append(y*640+x)  #MIGHT NOT BE RIGHT

    
    goodkp2 = []
    #convert 2D map to array map
    for m in match2:
        x, y =  kp[cameraNames[1]][m].pt

        x = Float2Int(x)
        y = Float2Int(y)

        goodkp2.append(y*640+x) #MIGHT NOT BE RIGHT


 
    

    print("good1",goodkp1)
    print("good2",goodkp2)

    
    
    #apenas usa pontos emparelhados
    XYZ1 = XYZline[cameraNames[0]][goodkp1] 
    XYZ2 = XYZline[cameraNames[1]][goodkp2]
    
    
    #inicializa highscore
    high_score_inliers = 0

    #RANSAC Loop

    

    #Procrustes
    perm = np.random.permutation(len(match1))
   
    print("perm",perm)


    #fetch 4  3D points from each camera
    #P1 = XYZ1[perm,:]
    #P2 = XYZ2[perm,:]

    P1 = []
    P2 = []
    i=0

    #remove invalid depth readings (the ones that are 0,0,0)
    while len(P1) < 4 and i<len(perm):

        if np.count_nonzero(XYZ1[perm[i],:])!=0 and np.count_nonzero(XYZ2[perm[i],:])!=0 :
            P1.append(XYZ1[perm[i],:])
            P2.append(XYZ2[perm[i],:])

        i=i+1

    P1 = np.asarray(P1)
    P2 = np.asarray(P2)
    

    pc1 = Points2Cloud(XYZline[cameraNames[0]],rgbline[cameraNames[0]])
    pc2 = Points2Cloud(XYZline[cameraNames[1]],rgbline[cameraNames[1]])
    pc3 = Points2Cloud(P1)
    pc4 = Points2Cloud(P2)

    print("p1",P1)
    print("p2",P2)
    

    #pc1.paint_uniform_color([1, 0.706, 0])
    #pc2.paint_uniform_color([0, 0.651, 0.929])
    pc3.paint_uniform_color([1, 0, 1])
    pc4.paint_uniform_color([1, 0, 0])
     
    
    #open3d.draw_geometries([pc3,pc4])

    mesh_sphere = open3d.create_mesh_sphere(radius = 0.3)
    mesh_sphere2 = open3d.create_mesh_sphere(radius = 0.3)
    mesh_sphere.paint_uniform_color([1, 0, 0])
    mesh_sphere2.paint_uniform_color([0, 1, 0])
    
    print("PPPP\n",P1[1,:])

    print("PPP2P\n",mesh_sphere.vertices)    

        
    #mesh_sphere.vertices =   open3d.Vector3dVector(P1[1,:]) + open3d.Vector3dVector(P1[1,:])
    #mesh_sphere2.vertices = mesh_sphere2.vertices + P2[1,:]

    mesh_sphere = open3d.geometry.create_mesh_coordinate_frame(origin=P1[2,:])
    mesh_sphere.paint_uniform_color([1, 0, 1])

    mesh_sphere2 = open3d.geometry.create_mesh_coordinate_frame(origin=P2[2,:])
    mesh_sphere2.paint_uniform_color([1, 0, 0])

    #print(mesh_sphere2.vertices=)
    open3d.draw_geometries([pc1,pc2,mesh_sphere,mesh_sphere2])

    '''
    print("Let\'s draw a cubic using LineSet")
    points = [P1,P2]
    lines = [[0,1],[0,2],[1,3],[2,3],
             [4,5],[4,6],[5,7],[6,7],
             [0,4],[1,5],[2,6],[3,7]]
    colors = [[1, 0, 0] for i in range(len(lines))]
    line_set = open3d.LineSet()
    line_set.points = open3d.Vector3dVector(points)
    line_set.lines = open3d.Vector2iVector(lines)
    line_set.colors = open3d.Vector3dVector(colors)
    open3d.draw_geometries([line_set])
    '''
    
    #VERIFIED UNTIL NOW

    print("Procrusted points",(P1.shape,P2))
  
    _,_,proctf = proc.procrustes(P1,P2,scaling=False,reflection=False)            
    rot = proctf["rotation"]
    XYZ2in1 = applyTransformation(XYZ2,rot,proctf["translation"])

    temp = XYZ2in1 - XYZ1
    norms = np.linalg.norm(temp,axis=1)
    Points2Cloud(XYZ1)
    #open3d.draw_geometries([Points2Cloud(XYZ1),Points2Cloud(XYZ2in1)])


    



    sio.savemat('np_vector.mat', {'rgb1':rgb[cameraNames[0]] ,'rgb2':rgb[cameraNames[1]] ,'XYZ1':XYZ[cameraNames[0]],'XYZ2':XYZ[cameraNames[1]], 'XYZ1emp':XYZ1,'XYZ2emp':XYZ2,'R':rot,'T':proctf["translation"],'P1':P1,'P2':P2})

    XYZ22in1 = applyTransformation(XYZline[cameraNames[1]],rot,proctf["translation"])

    #open3d.draw_geometries([Points2Cloud(XYZline[cameraNames[0]],rgbline[cameraNames[0]]),Points2Cloud(XYZ22in1,rgbline[cameraNames[1]])])

    print(norms)
    #fig = plt.figure()
    #plt.imshow(img3)
    #plt.show()
    #plt.draw()
    #plt.pause(2) # <-------
    #raw_input("<Hit Enter To Close>")
    #plt.close(fig)

def Float2Int(f):

    i = np.rint(f)
    i = i.astype(int) #nmpy round to int

    return i


def plotImg(img):
    fig = plt.figure()
    plt.imshow(img)
    plt.draw()
    plt.waitforbuttonpress(0) # this will wait for indefinite time
    plt.close(fig)



def applyTransformation(points,R,T):
    return  np.dot(points,R) + (np.ones([len(points),1])*T)

def Points2Cloud(points,rgb=None):
    #make point cloud    
    cloud = open3d.PointCloud()
    cloud.points = open3d.Vector3dVector(points)

    if(rgb is not None):
        cloud.colors = open3d.Vector3dVector(rgb/255.0) #range is 0-1 hence the division

    return cloud

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