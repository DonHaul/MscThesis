import math
import numpy as np


def CompareMatLists(matListA,matListB):
        #comparing with ground truth
    for i in range(0,len(matListA)):
        print(i)
        print("first")
        print(matListA[i])
        print("second")
        print(matListB[i])
        print("first - seconds")
        print(matListA[i]-matListB[i])

def PermuteCols(matList,permuter):
    finalR=[]
    for r in matList:
        finalR.append(np.dot(r,permuter))
    
    return finalR

def genRotMat(angle):


    angle = np.asarray(angle)   


    angle = angle*math.pi/180

    Rx = [[1,0,0],[0,math.cos(angle[0]),-math.sin(angle[0])],[0,math.sin(angle[0]),math.cos(angle[0])]]

    Ry = [[math.cos(angle[1]),0,math.sin(angle[1])],[0,1,0],[-math.sin(angle[1]),0,math.cos(angle[1])]]


    Rz = [[math.cos(angle[2]),-math.sin(angle[2]),0],[math.sin(angle[2]),math.cos(angle[2]),0],[0,0,1]] 

    aux = np.dot(Rx,Ry)


    return np.dot(aux,Rz)

    
'''
def genRotRel(rotsols):
    #print(ig.Nmarkers + ig.markerIDoffset)
    Rrelations = [[] for i in range(len(rotsols))] #correct way to make 2d list

    #generate R between each things
    for i in range(0,len(rotsols)):
        for j in range(0,len(rotsols)):
            Rrelations[i].append(np.dot(rotsols[j],rotsols[i].T)) ## ASSIM DA BEM MAS DEVIA SER -  Rrelations[i].append(np.dot(rotsols[j].T,rotsols[i]))

    return Rrelations
'''

def genRotRel(rotsols,ref=0):
    #print(ig.Nmarkers + ig.markerIDoffset)
    Rrelations = [] #correct way to make 2d list

    #generate R between each things
    for j in range(0,len(rotsols)):
        Rrelations.append(np.dot(rotsols[j],rotsols[ref].T)) #Rw2*R1w' = R12
    return Rrelations


def CheckSymmetric(a, tol=1e-8):
    return np.allclose(a, a.T, atol=tol)

def Rt2Homo(R,t):

    H = np.eye(4)

    H[0:3,0:3]=R
    H[0:3,3]=t


    return H
