"""
matmanip.py

This module is used to 
    manipulate matrices
    compare them
    check their properties
    Make rigid transformations
    and generate them
"""

import math
import numpy as np

def CompareMatLists(matListA,matListB):
    '''
    Compares 2 matrx lists

    Does:
        matListA - matListB
    '''
    
    #comparing with ground truth
    for i in range(0,len(matListA)):
        print(i)
        print("first")
        print(matListA[i])
        print("second")
        print(matListB[i])
        print("first - seconds")
        print(matListA[i]-matListB[i])

def PrintMatList(matlist):

    for i in range(0,len(matlist)):
        print("Mat "+str(i))
        print(matlist[i])



def genRandRotMatrix(noise):
    '''
    Generates a random matrix having into account the noise

    Args:
        noise: scale of the noise of the matrix to generate
    '''
    

    #generate noise
    a = np.random.rand(3,1)*noise

    #make it have 0 mean
    b =np.ones((3,1))*(noise/2)
    c=a-b


    return genRotMat(np.squeeze(c))

def genRotMat(angle):
    '''Generates a rotation matrix

    Args:
        angles [3x1]list: x,y,z euler angles in degrees of matrix to be generated

    Returns:
        R [3x3] float array :Rotation Matrix
    '''

    #converts to numpy array
    angle = np.asarray(angle)   

    #convert to radians
    angle = angle*math.pi/180

    #x angle rotation matrix
    Rx = [[1,0,0],[0,math.cos(angle[0]),-math.sin(angle[0])],[0,math.sin(angle[0]),math.cos(angle[0])]]
    #y angle rotation matrix
    Ry = [[math.cos(angle[1]),0,math.sin(angle[1])],[0,1,0],[-math.sin(angle[1]),0,math.cos(angle[1])]]
    #z angle rotation matrix
    Rz = [[math.cos(angle[2]),-math.sin(angle[2]),0],[math.sin(angle[2]),math.cos(angle[2]),0],[0,0,1]] 

    #mount the final rotation
    aux = np.dot(Rx,Ry)
    return np.dot(aux,Rz)

def isRotation(rotsols):
    '''
    Prints the properties of the rotation matrix
    '''
    #from world coordinates to ref coordinates

    #generate R between each things
    for j in range(0,len(rotsols)):
        print(np.linalg.det(rotsols[j]))
        print(np.dot(rotsols[j].T,rotsols[j]))
        
def genRotRelLeft(rotsols,ref=0):
    '''
    Multiplies matrix list by one of them on the left side

    Args:
        rotsols: list of matrices
        ref: which of those matrices will be multiplied on the left
    Returns:
        Rrelations: the multiplied matrices
    '''
    #from world coordinates to ref coordinates
    
    Rrelations = []

    #generate R between each things
    for j in range(0,len(rotsols)):
        Rrelations.append(np.dot(rotsols[ref].T,rotsols[j]))

    return Rrelations

def genRotRelRight(rotsols,ref=0):
    '''Rotates given matrics to be rotations relative to one them

    Does:
        R[i] = R w->i  Tranforms it into   R[i]= R ref->i 

    Args:
        rotsols list([3x3]) rotation matrices: list of all the rotation matrices to be rotated/transformed
        ref (int,optional): which of the matrices should they all be relative to? 
    '''
    
    Rrelations = []

    #generate R between each things
    for j in range(0,len(rotsols)):
        Rrelations.append(np.dot(rotsols[j],rotsols[ref].T)) #Rw2*R1w' = R12

    return Rrelations

def globalRotateRotsl(rotsols,ref=0):
    '''Rotates given matrics to be rotations relative to one them

    Does:
        R[i] = R w->i  Tranforms it into   R[i]= R ref->i 

    Args:
        rotsols list([3x3]) rotation matrices: list of all the rotation matrices to be rotated/transformed
        ref (int,optional): which of the matrices should they all be relative to? 
    '''
    
    Rrelations = []

    #generate R between each things
    for j in range(0,len(rotsols)):
        Rrelations.append(np.dot(rotsols[ref].T,rotsols[j])) #Rw2*R1w' = R12

    return Rrelations


def CheckSymmetric(a, tol=1e-8):
    '''
    Verifies if a matrix is symettric

    Args:
        a [matrix]: matrix to check symmetry on
        tol (float,optional): How close does it have to be

    Returns:
        Bool isSymetric
    '''
    return np.allclose(a, a.T, atol=tol)


def Rt2Homo(R=None,t=None):
    '''Creates Homography matrix from R and t

    Args:
        R [3x3]- rotation
        t [3x1]- tranlations
    Returns;
        H [4x4] - homography matrix
    '''
    
    if(R is None):
        R=np.eye(3)
    if(t is None):
        t= np.zeros((3,))

    H = np.eye(4)   #initializes H matrix
    H[0:3,0:3]=R    #sets R
    H[0:3,3]=t      #sets t

    return H

def Transposer(M):
    '''
    Receives matrix list where each matrix will be Transposed
    '''
    transposed = []
    for m in M:
        transposed.append(m.T)
    
    return transposed
    

def InvertT(R,t):
    '''Inverts translation, that is: t(1->2) transforms into t(2->1)
    
    Args:
        R [3x3]: Rotation of it
        t [3x1]: Translation of it
    Returns:
        inverted t
    '''
    return -np.dot(R.T,t)

def Transform(totransform,R,t):
    '''Transforms a t into another referential that is:
    t is in the i referential coordinates, it converts it to be in j referential coordinates    
    Args:
        totransform [3x1]: t to transform
        R[3x3]: R from i to j 
        t[3x1]: t from i to j
    Returns:
        transformedt[3x1]: in j coordinates
    '''

    if(len(totransform.shape)==1):
        totransform=np.expand_dims(totransform,axis=1)

    if(len(t.shape)==1):
        t=np.expand_dims(t,axis=1)

    return np.dot(R,totransform)+t

def InverseTransform(totransform,R,t):
    '''Inverts a certain transformation that is:
    R and t are from the i referential to the j onem it converts  to be from the j referential to the i one    
    Args:
        R[3x3]: R from i to j 
        t[3x1]: t from i to j
    Returns:
        R[3x3]: R from j to i 
        t[3x1]: t from j to i
    '''
    return np.dot(R.T,totransform)-np.dot(R.T,t)

def singlePixe2xyz(depth,coords,K):
    '''
    Gets the 3D position of a pixel in the image
    
    Args:
        depth: depth image
        coords: 2D coordinates to fetch the 3D from [x,y]
        K: intrinsics
    Returns:
        xyz: 3D position of that 2D point
    '''

    fx=K[0,0]
    fy=K[1,1]
    cx=K[0,2]
    cy=K[1,2]

    coords = np.round(coords)

    coords = coords.astype('int') 

    Z=depth[coords[1],coords[0]]/1000.0
    
    print(Z.shape)

    X=Z*(coords[0]-cx)/fx
    Y=Z*(coords[1]-cy)/fy
    #print("gayy")
    #print(np.array([X,Y,Z]))
    xyz= np.array([X,Y,Z])

    return xyz

def depthimg2xyz2(depthimg,K):
    '''
    Convert full depth image
    '''

    fx=K[0,0]
    fy=K[1,1]
    cx=K[0,2]
    cy=K[1,2]
    
    depthcoords = np.zeros((480, 640,3)) #height by width  by 3(X,Y,Z)

    u,v =np.indices((480,640))
    u=u-cy
    v=v-cx

    depthcoords[:,:,2]= depthimg/1000.0
    depthcoords[:,:,0]= depthcoords[:,:,2]*v/fx
    depthcoords[:,:,1]= depthcoords[:,:,2]*u/fy
    


    return depthcoords

def Transl_fromWtoRef(R,T,ref=0):
    '''
    Converts translation reference to one of a ref one

    Args:
        R: list of rotations
        T: list of translations
        ref: which referential shall be the new reference
    Returns:
        newT: translations in the new reference
    '''
    print("NEEDS UNIT TESTING FOR OTHER REFS")

    #from_to
    #tw_1 is  the invert of t1_w
    newT=[]
    # is is making ti_1 Rw_1*ti_w + tw_1
    for t in T:

        auxT = Transform(t,R[ref].T,InvertT(R[ref],T[ref]))
        newT.append(auxT)

    #print("doing shit")
    return newT


def depthimg2xyz(depthimg,rgb,K):

    fx=K[0,0]
    fy=K[1,1]
    cx=K[0,2]
    cy=K[1,2]
    
    depthcoords = np.zeros((480, 640,3)) #height by width  by 3(X,Y,Z)

    #u,v =np.indices((480,640))
    points=[]
    colors = []

    for v in range(depthimg.shape[1]):
        for u in range(depthimg.shape[0]):
            color = rgb[u,v,:] 
            Z = depthimg[u,v] / 1000.0
            if Z==0: continue

            X = (u - cx) * Z / fx
            Y = (v - cy) * Z / fy
            points.append([X,Y,Z])
            colors.append(color)



    return np.asarray(points),np.asarray(colors) 