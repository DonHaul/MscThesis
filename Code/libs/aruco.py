"""
aruco.py

This module contains aruco marker detection stuff
"""
import cv2
import numpy as np
import matmanip as mmnip
import algos

def markerIdMapper(arr):

    IdMap={}
    
    for i in range(0,len(arr)):
        IdMap[str(arr[i])]=i
    
    return IdMap

def ArucoObservationMaker(img,K,D,Nmarkers,arucoData,captureR=True,captureT=False):
    '''
    Finds Markers and makes observations

    Args:
        img: image to find aruco markers in
        K: intrinsic parameters
        D: distortion parameters
        markerIDoffset: shift from lowest id to 0
        Nmarkers: number of existing markers
        captureR (Bool): whether or not will be generated rotation observations
        captureT (Bool): whether or not will be generated translation observations

    Returns: 
        hello: image with detected markers and their referentials
        ids: detected ids
        obsR: observated Rotations
        obsT: observated translations
    '''

    #finds markers
    det_corners, ids, rejected = FindMarkers(img, K)

    #copy image
    hello = img.astype(np.uint8).copy() 

    #draw maerkers
    hello = cv2.aruco.drawDetectedMarkers(hello,det_corners,ids)

    #make observations, and draw referentials
    obsR,obsT,hello = ObservationMaker(K,D,det_corners,hello,ids,arucoData,captureR,captureT)

    return hello ,ids,obsR,obsT #<- ids parameter doenst need to be here - WRONG

def ObservationMaker(K,D,det_corners,img,ids,arucoData,captureR=True,captureT=False):
    '''
    Generates Observations

    Args:
        K: intrinsic camera matrix
        D: distortion parameters
        det_corners: all detected corners
        hello: img
        ids: all detected ids
    Returns:
        observationsR: rotation observations
        observationsT: tranlation observations
        img: img with markers and referentials in it
    '''
    
    observationsR = []
    observationsT = []

    #if more than one marker was detected
    if  ids is not None and len(ids)>1:

        #finds rotations and vectors and draws referentials on image
        rots,tvecs,img = FindPoses(K,D,det_corners,img,len(ids),arucoData['size'])
        #this rots and tvecs are in camera coordinates

        #squeeze
        ids = ids.squeeze()



        #generates samples
        for i in range(0,len(ids)):                
            for j in range(i+1,len(ids)):
                
                #only valid markers
                if ids[i] not in arucoData['ids']:
                    print("Invalid marker id: "+str(ids[i]))
                    continue 

                                 #only valid markers
                if ids[j] not in arucoData['ids']:
                    print("Invalid marker id: "+str(ids[i]))
                    continue 

                #print("observing "+str(i)+" and "+str(j))

                #generate R observations
                if(captureR):
                    #obsR={"to":(ids[i]+markerIDoffset),"from":(ids[j]+markerIDoffset),"R":np.dot(rots[i].T,rots[j])} #THE CORRECT WAY
                    obsR={"to":arucoData['idmap'][str(ids[i])],"from":arucoData['idmap'][str(ids[j])],"R":np.dot(rots[i].T,rots[j])}
                    observationsR.append(obsR)
                
                
                
                if(captureT):
                    #generate t observations
                    obsT={"from":arucoData['idmap'][str(ids[i])],"to":arucoData['idmap'][str(ids[j])],"t":np.squeeze(np.dot(rots[j].T,(tvecs[i]-tvecs[j]).T))} 
                    observationsT.append(obsT)


    return observationsR , observationsT ,img


def FindMarkers(img,K):
    '''Detects aruco markers in an image

    Args:
        img: image to extract markers from
        K: camera intrinsic parameters
    '''  

    #What type of aruco markers are there
    adict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_ARUCO_ORIGINAL)

    #make the image grey
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    #get markers
    det_corners, ids, rejected  = cv2.aruco.detectMarkers(gray,dictionary=adict,cameraMatrix=K)

    return det_corners, ids, rejected


def FindPoses(K,D,det_corners,img,n,size):
    '''
    Estimates rotation and translation of each aruco

    Args:
        K: intrinsic parameters
        D: distortion parameters
        det_corners:detected corners
        img: image to draw axis on
        n: number of detected ids
    '''

    #get pose
    rvecs, tvecs, _ = cv2.aruco.estimatePoseSingleMarkers(det_corners,size,K,D)

    #the third parameter is corner coordinates


    #for r in rvecs
    rots = []

    for i in range(n):

        #converts to 3x3 rotation matrix
        elm,_ = cv2.Rodrigues(rvecs[i,0,:])
        #cv2.Rodrigues(src=rvecs[i,0,:])
        rots.append(elm)

        #draws axis
        img = cv2.aruco.drawAxis(img,K,D,elm,tvecs[i],0.1)

    ola = np.asarray(rots)

    return rots,tvecs,img

def GetCangalhoFromMarkersProcrustes(ids,det_corners,K,arucoData,arucoModel,depth_reg):

    #because there are 4 corners per detected aruco
    pointsModel=np.empty((0,3))

    points3D=np.empty((0,3))

    #print("ids are")
    #print(ids)
    #print(det_corners)



    for i in range(len(ids)):

        cor = np.squeeze(det_corners[i])

        corns3D = Get3DCorners(ids[i],arucoData,arucoModel)

        #print(np.squeeze(det_corners[i]))
        for j in range(0,4):
            
            point = mmnip.singlePixe2xyz(depth_reg,cor[j],K)

            if point[2]==0:
                print("THIS POINT IS INVALID")
                continue

            points3D = np.vstack((points3D,point))
            pointsModel = np.vstack((pointsModel,corns3D[j]))
    
    #print("3D POINTS AND SHIET")
    #print(points3D.shape)

    if(points3D.shape[0]<4):
        return None

    #print(pointsModel.shape)
    #Rr,tt
    return algos.procrustesMatlabJanky2(points3D,pointsModel)



def Get3DCorners(id,arucoData,arucoModel):

    mappedID = arucoData['idmap'][str(int(id))]


    c1 = np.array([-arucoData['size']/2,arucoData['size']/2,0])
    c2 = np.array([arucoData['size']/2,arucoData['size']/2,0])
    c3 = np.array([arucoData['size']/2,-arucoData['size']/2,0])
    c4 = np.array([-arucoData['size']/2,-arucoData['size']/2,0])

    corn1 = mmnip.Transform(c1,arucoModel['R'][mappedID],arucoModel['T'][mappedID])
    corn2 = mmnip.Transform(c2,arucoModel['R'][mappedID],arucoModel['T'][mappedID])
    corn3 = mmnip.Transform(c3,arucoModel['R'][mappedID],arucoModel['T'][mappedID])
    corn4 = mmnip.Transform(c4,arucoModel['R'][mappedID],arucoModel['T'][mappedID])


    corn1= np.squeeze(corn1)
    corn2= np.squeeze(corn2)
    corn3= np.squeeze(corn3)
    corn4= np.squeeze(corn4)

    return [corn1,corn2,corn3,corn4]

def GetCangalhoFromMarkersPnP(ids,det_corners,K,arucoData,arucoModel):

    #because there are 4 corners per detected aruco
    image_points=np.zeros((4*len(ids),2))

    points3D=np.zeros((4*len(ids),3))

    for i in range(len(ids)):


        mappedID = arucoData['idmap'][str(int(ids[i]))]

        #FROM CORNERS TO RGB
        #FROM CORNERS TO RGB

        c1 = np.array([-arucoData['size']/2,arucoData['size']/2,0])
        c2 = np.array([arucoData['size']/2,arucoData['size']/2,0])
        c3 = np.array([arucoData['size']/2,-arucoData['size']/2,0])
        c4 = np.array([-arucoData['size']/2,-arucoData['size']/2,0])

        

        corn1 = mmnip.Transform(c1,arucoModel['R'][mappedID],arucoModel['T'][mappedID])
        corn2 = mmnip.Transform(c2,arucoModel['R'][mappedID],arucoModel['T'][mappedID])
        corn3 = mmnip.Transform(c3,arucoModel['R'][mappedID],arucoModel['T'][mappedID])
        corn4 = mmnip.Transform(c4,arucoModel['R'][mappedID],arucoModel['T'][mappedID])


        corn1= np.squeeze(corn1)
        corn2= np.squeeze(corn2)
        corn3= np.squeeze(corn3)
        corn4= np.squeeze(corn4)

        corn3D = np.vstack((corn1,corn2,corn3,corn4))


        points3D[i*4:i*4+4,:] = corn3D
        
        #print("corners swapped")
        #print(np.flip(np.squeeze(det_corners[i]),axis=1))
        image_points[i*4:i*4+4,:]=np.squeeze(det_corners[i])
        


    if (points3D.shape[0]==0):
        return None,None


    retval, orvec, otvec = cv2.solvePnP(points3D,image_points,K,None, flags = cv2.SOLVEPNP_ITERATIVE)

    rvec,_ = cv2.Rodrigues(orvec)

    return rvec,otvec

    