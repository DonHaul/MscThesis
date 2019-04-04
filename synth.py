import open3d
import math
import numpy as np
import pickler as pickle
import pprint
import random
import Rtmat
import phase2_sparkle as phase2


def FetchKeyArray(key,dictlist):
    return [d[key] for d in dictlist]

def main():

    refs=[]

    R,t = FakeAruco()


    #ViewRefs(R,t)

    
   
    #obs = SampleGeneratorMin(R)

    obsR,obst = SampleGenerator(R,t,noise=1)
    

    B = phase2.problemDef(obsR,len(R))

    ola = np.dot(B.T,B)

    #checked seen here

    rotSols = phase2.TotalLeastSquares(ola,3,len(R))
    



    
    ViewRefs(rotSols)

    rotSoles = Rtmat.genRotRel(rotSols)

    for i in range(len(rotSoles)/4):
        ViewRefs(rotSoles[i*4])

    print("yo",rotSoles)

    print("lol",rotSoles[0])

        # TRANSLATION STUFF
    B = problemDef2(obst,rotSoles,len(t))

    ola = np.dot(B.T,B)


    TotalLeastSquaresT(ola,1,len(R))
    #################


    #ViewRefs(rotSoles[0])

def problemDef2(observations,rotRel,N):

    #creates the left matrix in the problem formulation
    Ident = np.zeros((len(observations)*4,N*4))


    #creates the right matrix in the problem formulatin
    A = np.zeros((len(observations)*4,N*4))
            
    cnt = 0
    for obs in observations:
        #fills the matrices according to the observed pairs
        Ident[cnt*4:cnt*4+4,obs['to']*4:obs['to']*4+4]= np.eye(4)
        A[cnt*4:cnt*4+3,obs['from']*4:obs['from']*4+3]=  rotRel[obs['from']][obs['to']]

        A[cnt*4+3,obs['from']*4+3]=1

        A[cnt*4+3,obs['from']*4:obs['from']*4+3]= obs['trans']

        cnt=cnt+1
    
    return Ident - A

def SampleGeneratorMin(rot,noise = 1e-10):

    obs=[]

    for i in range(0,len(rot)-1):
        #SHOULDNT IT BE rot[i+1],rot[i+1].T)
        obs.append({"from":i,"to":i+1,"rot":np.dot(np.dot(rot[i+1],rot[i].T),Rtmat.genRotMat(np.squeeze([np.random.rand(3,1)*noise])))})   
        #print(i,i+1)

    obs.append({"from":len(rot)-1,"to":0,"rot":np.dot(rot[0],rot[len(rot)-1].T)})  #delete this line after
    return obs


def SampleGenerator(R,t,samples=1000,noise = 0.00001,noiset=0.0001):

    
    r = np.zeros([len(R),1])

    while True:

        obsR = []
        obst = []

        for i in range(0,samples):

            #for each observation        

            #pick 2 different ids
            r1 =  random.randint(0, len(R)-1)
            r2 = r1
            while r2==r1:
                r2 = random.randint(0, len(R)-1)

            
            obsR.append({"from":r2,"to":r1,"rot":np.dot(np.dot(R[r1],R[r2].T),Rtmat.genRotMat(np.squeeze([np.random.rand(3,1)*noise])))})
            obst.append({"from":r2,"to":r1,"trans":np.squeeze(t[0]-t[1] + np.random.rand(1,3)*noiset)})

            r[r1]=1
            r[r2]=1

        #print(sum(r))
        #there is at least one observation per marker
        if sum(r)==len(R):
            break

    return obsR,obst
    


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


def TotalLeastSquaresT(C,Nleast,split):
    '''
    ola
    '''

    u,s,vh = np.linalg.svd(C)
    
    solution = u[:,-Nleast:]

    #split in 3x3 matrices, dat are close to the rotation matrices but not quite
    rotsols = []
    solsplit = np.split(solution,split)

    return solsplit
    
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
    
    t.append(np.array([0,10,10]))
    t.append(np.array([0,30,10]))
    t.append(np.array([0,50,10]))

    t.append(np.array([10,10,0]))
    t.append(np.array([10,30,0]))
    t.append(np.array([10,50,0]))

    t.append(np.array([0,10,-10]))
    t.append(np.array([0,30,-10]))
    t.append(np.array([0,50,-10]))

    t.append(np.array([-10,10,0]))
    t.append(np.array([-10,30,0]))
    t.append(np.array([-10,50,0]))

    return R,t






if __name__ == '__main__':
    main()
