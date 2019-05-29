"""
aruco.py

This module contains aruco marker detection stuff
"""
import cv2
import numpy as np
import matmanip as mmnip
import algos

def markerIdMapper(arr):
    '''
    Maps markers from the ones in the aruco to the ones starting in 0

    Args:
        arr: the array of ids

    Returns:
        IdMaps: dictionary that maps aruco ids, to the ones from 0 to whatever
    '''

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


def FindMarkers(img,K,D=np.asarray([0,0,0,0])):
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
    det_corners, ids, rejected  = cv2.aruco.detectMarkers(gray,dictionary=adict,cameraMatrix=K,distCoeff=D)

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
    Returns:
        rots: rotations of the markers
        tvecs: translations of the markers
        img: images
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
    '''
    Estimates rotation and translation of the full cangalho aruco

    Args:
        ids: the arucos detected in a given image
        det_corners: the corners of the detected markers
        K: intrinsic parameters
        arucoData: holds the size of the arucos inside
        arudcoModel: relative pose between markers in the aruco model
        depth_reg: depth image
    Returns:
        R: rotations of the aruco markers
        t: translations of the aruco markers
    '''

    #because there are 4 corners per detected aruco
    pointsModel=np.empty((0,3))

    #holds the corners from the model
    points3D=np.empty((0,3))

    #cicles all ids
    for i in range(len(ids)):

        cor = np.squeeze(det_corners[i])

        #fetches the corners 3D in the aruco model
        corns3D = Get3DCorners(ids[i],arucoData,arucoModel)

        
        for j in range(0,4):
            
            #gets the detected corner in the current depth image
            point = mmnip.singlePixe2xyz(depth_reg,cor[j],K)

            #skip if it is invalid (if there is no depth on this point)
            if point[2]==0:
                print("THIS POINT IS INVALID")
                continue    

            #add the the stack the valid corners
            points3D = np.vstack((points3D,point))
            pointsModel = np.vstack((pointsModel,corns3D[j]))
    
    #the procrustes only works with 4 or more points
    if(points3D.shape[0]<4):
        return None

    #makes procrutes with the valid points
    return algos.procrustesMatlabJanky2(points3D,pointsModel)



def Get3DCorners(id,arucoData,arucoModel):
    '''
    Gets 3D positions of the corners of a given marker

    Args:
        id: if of that marker
        arucoData: holds the size of the arucos
        arudcoModel: relative pose between markers in the aruco model, used to get rotation and translation of the detected marker
    Returns:
        corners: 3D positions of the corners of the selected marker
    '''

    mappedID = arucoData['idmap'][str(int(id))]


    c1 = np.array([-arucoData['size']/2,arucoData['size']/2,0])     #canto superior esquerdo relativo ao centro do marker
    c2 = np.array([arucoData['size']/2,arucoData['size']/2,0])      #canto superior direito relativo ao centro do marker
    c3 = np.array([arucoData['size']/2,-arucoData['size']/2,0])     #canto inferior direito relativo ao centro do marker
    c4 = np.array([-arucoData['size']/2,-arucoData['size']/2,0])    #canto inferior esquerdo relativo ao centro do marker

    #get the actual 3D position on the model
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
    '''
    Estimates rotation and translation of the full cangalho aruco

    Args:
        ids: the arucos detected in a given image
        det_corners: the corners of the detected markers
        K: intrinsic parameters
        arucoData: holds the size of the arucos inside
        arudcoModel: relative pose between markers in the aruco model
    Returns:
        R: rotations of the aruco markers
        t: translations of the aruco markers
    '''

    #because there are 4 corners per detected aruco
    image_points=np.zeros((4*len(ids),2))

    #the corners in the actual moel
    points3D=np.zeros((4*len(ids),3))

    for i in range(len(ids)):


        corns = Get3DCorners(i,arucoData,arucoModel)
        


        corn1= corns[0]
        corn2= corns[1]
        corn3= corns[2]
        corn4= corns[3]

        corn3D = np.vstack((corn1,corn2,corn3,corn4))


        points3D[i*4:i*4+4,:] = corn3D
        
        #adds the image points
        image_points[i*4:i*4+4,:]=np.squeeze(det_corners[i])
        

    #if no ids were found, dont return things
    if (points3D.shape[0]==0):
        return None,None

    #solve the point n perspective issue
    retval, orvec, otvec = cv2.solvePnP(points3D,image_points,K,None, flags = cv2.SOLVEPNP_ITERATIVE)

    #get the 3D matrix
    rvec,_ = cv2.Rodrigues(orvec)

    return rvec,otvec

    