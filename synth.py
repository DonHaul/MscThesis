import open3d
import math
import numpy as np
import pickler as pickle
import pprint
import random
import Rtmat
import phase2_sparkle as phase2


def main():

    refs=[]

    R,t = FakeAruco()

    #ViewRefs(R,t)

   
    #obs = SampleGeneratorMin(R)

    obs = SampleGenerator(R,noise=10)
    
    B = phase2.problemDef(obs,len(R))

    ola = np.dot(B.T,B)

    #checked seen here

    rotSols = phase2.TotalLeastSquares(ola,3,len(R))

    
    ViewRefs(rotSols)

    rotSoles = Rtmat.genRotRel(rotSols)

    print("yo",rotSoles)

    print("lol",rotSoles[0])

    #ViewRefs(rotSoles[0])


def SampleGeneratorMin(rot,noise = 1e-10):

    obs=[]

    for i in range(0,len(rot)-1):
        #SHOULDNT IT BE rot[i+1],rot[i+1].T)
        obs.append({"from":i,"to":i+1,"rot":np.dot(rot[i+1],rot[i].T)+Rtmat.genRotMat(np.squeeze([np.random.rand(3,1)*noise]))})   
        #print(i,i+1)

    obs.append({"from":len(rot)-1,"to":0,"rot":np.dot(rot[0],rot[len(rot)-1].T)})  #delete this line after
    return obs


def SampleGenerator(R,samples=1000,noise = 0.00001):

    
    r = np.zeros([len(R),1])

    while True:

        obs = []

        for i in range(0,samples):

            #for each observation        

            #pick 2 different ids
            r1 =  random.randint(0, len(R)-1)
            r2 = r1
            while r2==r1:
                r2 = random.randint(0, len(R)-1)

            
            obs.append({"from":r2,"to":r1,"rot":np.dot(R[r1],R[r2].T)+Rtmat.genRotMat(np.squeeze([np.random.rand(3,1)*noise]))})            
            
            r[r1]=1
            r[r2]=1

        #print(sum(r))
        #there is at least one observation per marker
        if sum(r)==len(R):
            break

    return obs
    


def ViewRefs(R,t=None):



    refs = []

    if t is None:
        t = []
        for i in range(0,len(R)):
            t.append([i*20,0,0]) 


    

    for i in range(len(R)):

        P=np.eye(4)

        
        P[0:3,0:3]= R[i]
        P[0:3,3]=t[i]

        refe = open3d.create_mesh_coordinate_frame(size = 10, origin = [0, 0, 0])
        refe.transform(P)

        refs.append(refe)

    open3d.draw_geometries(refs)

    return refs



def GenReferential(angle,t):

    refe = open3d.create_mesh_coordinate_frame(size = 10, origin = [0, 0, 0])
    
    refe.transform(P)

    return refe

    

def FakeAruco():

    R=[]
    t=[]

    R.append(Rtmat.genRotMat([0,0,0]))
    R.append(Rtmat.genRotMat([0,0,0]))
    R.append(Rtmat.genRotMat([0,0,0]))

    R.append(Rtmat.genRotMat([0,90,0]))
    R.append(Rtmat.genRotMat([0,90,0]))
    R.append(Rtmat.genRotMat([0,90,0]))
    
    R.append(Rtmat.genRotMat([0,180,0]))
    R.append(Rtmat.genRotMat([0,180,0]))
    R.append(Rtmat.genRotMat([0,180,0]))

    R.append(Rtmat.genRotMat([0,270,0]))
    R.append(Rtmat.genRotMat([0,270,0]))
    R.append(Rtmat.genRotMat([0,270,0]))
    
    t.append([0,10,10])
    t.append([0,30,10])
    t.append([0,50,10])

    t.append([10,10,0])
    t.append([10,30,0])
    t.append([10,50,0])

    t.append([0,10,-10])
    t.append([0,30,-10])
    t.append([0,50,-10])

    t.append([-10,10,0])
    t.append([-10,30,0])
    t.append([-10,50,0])

    return R,t






if __name__ == '__main__':
    main()
