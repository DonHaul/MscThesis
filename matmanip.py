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

def AxisSwapper(matlist,permuter):
    

    finalR=  PermuteCols(matlist,permuter)  

    #print("finalR")
    #visu.ViewRefs(finalR)


    
    Rrelations = []
    #generate R between each things
    for j in range(0,len(finalR)):
        Rrelations.append(np.dot(finalR[0].T,finalR[j])) #Rw2*R1w' = R12

    return Rrelations


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

def PermuteCols(matList,permuter):
    '''Permutes columns of matrices of a list:
    
    Does:
        matList[i]*permuter

    Args:
        matList [Nx3]: matrices to permute columns
        permuter [3x3]: permuter matrix

    Returns:
        finalR [Nx3]: matrices with permutated columns   
    '''

    finalR=[]
    for r in matList:
        finalR.append(np.dot(r,permuter))
    
    return finalR

def PermuteRows(matList,permuter):
    '''Permutes columns of matrices of a list:
    
    Does:
        matList[i]*permuter

    Args:
        matList [Nx3]: matrices to permute columns
        permuter [3x3]: permuter matrix

    Returns:
        finalR [Nx3]: matrices with permutated columns   
    '''

    finalR=[]
    for r in matList:
        finalR.append(np.dot(permuter,r))
    
    return finalR

def genRandRotMatrixMultiNoise(noise):

    #print("noise is:"+str(noise))

    #generate noise
    a = np.random.rand(3,1)*noise

    noises = []

    for n in noise:
        a=a*n

        #make it have 0 mean
        b =np.ones((3,1))*(n/2)
        c=a-b

        noises.append(genRotMat(np.squeeze(c)))
    #print("a")
    #print(a)
    #print(a.shape)
    #print("b")
    #print(b)
    #print(b.shape)
    #print("c")
    #print(c)
    #print(c.shape)

    return  noises

def genRandRotMatrix(noise):

    #print("noise is:"+str(noise))

    #generate noise
    a = np.random.rand(3,1)*noise

    #make it have 0 mean
    b =np.ones((3,1))*(noise/2)
    c=a-b
    #print("a")
    #print(a)
    #print(a.shape)
    #print("b")
    #print(b)
    #print(b.shape)
    #print("c")
    #print(c)
    #print(c.shape)

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

def genRotRelLeft(rotsols,ref=0):
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


def Rt2Homo(R,t):
    '''Creates Homography matrix from R and t

    Args:
        R [3x3]- rotation
        t [3x1]- tranlations
    Returns;
        H [4x4] - homography matrix
    '''

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

def depthimg2xyz(depthimg,K):

    fx=K[0,0]
    fy=K[1,1]
    cx=K[0,2]
    cy=K[1,2]
    
    depthcoords = np.zeros((480, 640,3)) #height by width  by 3(X,Y,Z)

    u,v =np.indices((480,640))
    
    u=u-cx
    v=v-cy

    depthcoords[:,:,2]= depthimg/1000.0
    depthcoords[:,:,0]= depthcoords[:,:,2]*v/fx
    depthcoords[:,:,1]= depthcoords[:,:,2]*u/fy

    return depthcoords