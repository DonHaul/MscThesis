import open3d
import math
import numpy as np
import pickler as pickle
import pprint
import random
import matmanip as mmnip
import phase2_sparkle as phase2
from visu import *


def main():

    
    refs=[]

    #Verified
    R,t = FakeAruco()

    #Verified
    ViewRefs(R,t)

    groundTruths = mmnip.genRotRel(R)
    
    #ViewRefs(groundTruths[0])

    

    
   
   

    obsR,obst = SampleGenerator(R,t,noise=1)
    
    #print(obst)

    B = phase2.problemDef(obsR,len(R))

    ola = np.dot(B.T,B)

    #checked seen here

    rotSols = phase2.TotalLeastSquares(ola,3,len(R))
    
    print("global")

    ViewRefs(rotSols)

    #very janky
    rotSoles = Rtmat.genRotRel(rotSols)
    print("local")
    ViewRefs(rotSoles[0])
    
 
    quit()
    
    print("YAOZA")

    



    rotS2 = []
    for r in rotSoles[0]:
        rotS2.append(np.dot(r,Rtmat.genRotMat([90,0,0])))
    ViewRefs(rotS2)

    rotS3 = []
    for r in rotS2:
        rotS3.append(np.dot(Rtmat.genRotMat([-90,0,0]),r))
    ViewRefs(rotS3)


        

    # TRANSLATION STUFF
    A,b = problemDef2(obst,rotS3,len(t))

    x, res, rank, s = np.linalg.lstsq(A,b,rcond=None) #(A'A)^(-1) * A'b


    #print(x,res,rank,s)    

    x2= np.dot( np.linalg.inv(np.dot(A.T,A)),np.dot(A.T,b)) #(A'A)^(-1) * A'b

    pprint.pprint(sum(np.square(np.dot(A,x)-b)) )
    pprint.pprint(sum(np.square(np.dot(A,x2)-b)))

    #JANKY
    solsplit2 = np.split(x,len(t))

    print(solsplit2[0].shape)


    ViewRefs(rotS3,solsplit2,refSize=1)

    #ViewRefs(None,[np.array([3,1,2]),np.array([3,1,1]),np.array([3,1,0])])

    

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

            obsR.append({"from":r2,"to":r1,"R":np.dot(mmnip.genRotMat(np.squeeze([np.random.rand(3,1)*noise])),np.dot(R[r1],R[r2].T))})
            obst.append({"from":r1,"to":r2,"t":t12+np.random.rand(3)}) #*noiset
            #print(obst)
            r[r1]=1
            r[r2]=1


        #print(sum(r))
        #there is at least one observation per marker
        if sum(r)==len(R):
            break

    return obsR,obst
    

   
def FakeAruco():

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






if __name__ == '__main__':
    main()
