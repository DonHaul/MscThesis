import math
import numpy as np



def genRotMat(angle):


    angle = np.asarray(angle)   


    angle = angle*math.pi/180

    Rx = [[1,0,0],[0,math.cos(angle[0]),-math.sin(angle[0])],[0,math.sin(angle[0]),math.cos(angle[0])]]

    Ry = [[math.cos(angle[1]),0,math.sin(angle[1])],[0,1,0],[-math.sin(angle[1]),0,math.cos(angle[1])]]


    Rz = [[math.cos(angle[2]),-math.sin(angle[2]),0],[math.sin(angle[2]),math.cos(angle[2]),0],[0,0,1]] 

    aux = np.dot(Rx,Ry)


    return np.dot(aux,Rz)

    

def genRotRel(rotsols):
    #print(ig.Nmarkers + ig.markerIDoffset)
    Rrelations = [[] for i in range(len(rotsols))] #correct way to make 2d list

    #generate R between each things
    for i in range(0,len(rotsols)):
        for j in range(0,len(rotsols)):
            Rrelations[i].append(np.dot(rotsols[j],rotsols[i].T)) ## ASSIM DA BEM MAS DEVIA SER -  Rrelations[i].append(np.dot(rotsols[j].T,rotsols[i]))

    return Rrelations


def CheckSymmetric(a, tol=1e-8):
    return np.allclose(a, a.T, atol=tol)