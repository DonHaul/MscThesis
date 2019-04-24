import open3d
import math
import numpy as np
import pickler as pickle
import pprint
import random
import matmanip as mmnip
from visu import *

    

def SampleGenerator(R,t,samples=1000,noise = 0.00001,noiset=0.0001):
    '''
    returns observationsR, and observationsT
    '''

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
            

            #t1w = (np.expand_dims(t[r1],0).T) # ref 1 no referencial do mundo
            #t2w = (np.expand_dims(t[r2],0).T) # ref 2 no referencial do mundo
            
            #tw2 = np.dot(-R[r2],t2w) # ref do mundo no referencial do 2
            #tw1 = np.dot(-R[r1],t1w) # ref do mundo no referencial do 1

            #t12=tw1 - np.dot(np.dot(R[r1],R[r2].T),tw2)
            #print("#### # #### from "+ str(r1) + " to "+ str(r2))
          
            #tw1 = np.dot(-R[r1].T,t[r1]) # <-- NAO ERA SUPOSTO TER O TRANSPOSTO WRONG / understand WHY
            #print(tw1)

            #tw2 = np.dot(-R[r2].T,t[r2]) # <-- NAO ERA SUPOSTO TER O TRANSPOSTO WRONG / understand WHY

            t1w = t[r1]
            t2w = t[r2]

            

            t12 =np.dot(R[r2].T, t1w - t2w)

            
            #print(str(r1)+" in w coords",t[r1])
            #print(str(r2)+" in w coords",t[r2])
            #print(str(r1)+ "  in " + str(r2) + " coordinates: "+ str(t12))
            #raw_input()

            #t21=tw1-np.dot(np.dot(R[r1],R[r2].T),tw2)
            #print(t21)
            #print(t12.shape)
            obsR.append({"from":r2,"to":r1,"R":np.dot(mmnip.genRotMat(np.squeeze([np.random.rand(3,1)*noise])),np.dot(R[r1],R[r2].T))})
            obst.append({"from":r1,"to":r2,"t":t12+np.random.rand(3)*noiset}) #*noiset
            #print({"from":r2,"to":r1,"R":np.dot(R[r1],R[r2].T)})
            #raw_input()
            r[r1]=1
            r[r2]=1


        #print(sum(r))
        #there is at least one observation per marker
        if sum(r)==len(R):
            break

    return obsR,obst




#attention this does not check if all cameras have matches
def MultiCamSampleGeneratorFixed(Rcam,tcam,R,t,nObs=5):
    '''
    simulates one single frame in every camera and matches results
    '''
     #number of observations of a camera in a certain frame

    if(nObs>len(tcam)):
        print("Warning: Number of observations requested higher than total markers")
        nObs=len(tcam)-1

    camsObs = []

    noise = 0.01
    noiset = 0.01
    
    #generate SingleCam Samples
    for i in range(0,len(Rcam)):
        
        #pick random ones
        rnds = random.sample(range(1, len(R)), nObs)

        obs=[]
        

        for r in rnds:
            
            tcr =np.dot(Rcam[i].T, t[r] - tcam[i]) # t from observation r to camera i  


            #generate the samples  'from' Camera i 'to' sample i
            #'ObsId' = 'to'                 #'camId = to ObsId = 'from'
            #assign them to each camera
            o ={"obsId":r,"R": np.dot(mmnip.genRotMat(np.squeeze([np.random.rand(3,1)*noise])), np.dot(R[r],Rcam[i].T)),'t':tcr}
            obs.append(o)

            #print("fromMarker:"+str(o['obsId'])+" toCamera:"+str(i)) - CORRECT
            #print(tcr)
            #raw_input()
    
        camsObs.append(obs)



    return camsObs

def Scenev1():

    R=[]
    t=[]

    R.append(mmnip.genRotMat([0,180,0]))
    R.append(mmnip.genRotMat([0,-90,0]))
    R.append(mmnip.genRotMat([0,0,0]))

    t.append(np.array([0,0,0]))
    t.append(np.array([50,0,-50]))
    t.append(np.array([0,0,-100]))

    return R,t

def FakeArucoRotated():

    R=[]
    t=[]

    R.append(mmnip.genRotMat([90,180,0]))
    R.append(mmnip.genRotMat([90,90,0]))
    R.append(mmnip.genRotMat([90,0,0]))
    R.append(mmnip.genRotMat([90,-90,0]))
    
    t.append(np.array([0,10,0]))
    t.append(np.array([10,0,0]))
    t.append(np.array([0,-10,0]))
    t.append(np.array([-10,0,0]))

    return R,t


def FakeAruco():

    R=[]
    t=[]

    R.append(mmnip.genRotMat([0,0,0]))
    R.append(mmnip.genRotMat([0,90,0]))
    R.append(mmnip.genRotMat([0,180,0]))
    R.append(mmnip.genRotMat([0,270,0]))
    
    t.append(np.array([0,0,10]))
    t.append(np.array([10,0,0]))
    t.append(np.array([0,0,-10]))
    t.append(np.array([-10,0,0]))

    return R,t

   
def FakeArucoReal():

    R=[]
    t=[]

    R.append(mmnip.genRotMat([0,0,0]))
    R.append(mmnip.genRotMat([0,0,0]))
    R.append(mmnip.genRotMat([0,0,0]))

    R.append(mmnip.genRotMat([0,90,0]))
    R.append(mmnip.genRotMat([0,90,0]))
    R.append(mmnip.genRotMat([0,90,0]))
    
    R.append(mmnip.genRotMat([0,180,0]))
    R.append(mmnip.genRotMat([0,180,0]))
    R.append(mmnip.genRotMat([0,180,0]))

    R.append(mmnip.genRotMat([0,270,0]))
    R.append(mmnip.genRotMat([0,270,0]))
    R.append(mmnip.genRotMat([0,270,0]))
    
    t.append(np.array([0,0,10]))
    t.append(np.array([0,30,10]))
    t.append(np.array([0,50,10]))

    t.append(np.array([10,0,0]))
    t.append(np.array([10,30,0]))
    t.append(np.array([10,50,0]))

    t.append(np.array([0,0,-10]))
    t.append(np.array([0,30,-10]))
    t.append(np.array([0,50,-10]))

    t.append(np.array([-10,0,0]))
    t.append(np.array([-10,30,0]))
    t.append(np.array([-10,50,0]))

    return R,t






