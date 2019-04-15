import open3d
import math
import numpy as np
import pickler as pickle
import pprint
import random
import Rtmat
import phase2_sparkle as phase2
from synth import *



def main():

    np.set_printoptions(threshold=np.inf)
    np.set_printoptions(precision=1)

    R=[]
    t=[]


    R,t = FakeAruco()

    pprint.pprint(t)

    ViewRefs(R,t)
    
    obsR,obst = SampleGenerator(R,t,noise=0.1,noiset=0,samples=10000)

    '''
    for i in obst:
        print("From: " +str(i['from']//3+1)+" to:"+str(i['to']//3+1))
        print(i)

        ViewRefs([Rtmat.genRotMat([0,0,0]),i['trans']])
    '''

        # TRANSLATION STUFF
    A,b = problemDef2(obst,R,len(t))

    x, res, rank, s = np.linalg.lstsq(A,b,rcond=None) #(A'A)^(-1) * A'b
    #print(x,res,rank,s) 
    

    print("asahpe",np.dot(A.T,A).shape)

    x2= np.dot( np.linalg.pinv(np.dot(A.T,A)),np.dot(A.T,b)) #(A'A)^(-1) * A'b  #<= WHY USE PINV INSTEAD OF INV (WRONG?)
    #print(x2)

    print( "DIFFERENCE", sum(np.sqrt(np.square(x-x2))))

    
    print("x")
    #print(x2)
    #JANKY
    solsplit2 = np.split(x2,len(t))
    
    solt =[]

    for i in range(len(solsplit2)):
        solt.append(np.dot(-R[i].T,solsplit2[i]))
 
    pprint.pprint(solt)


    ViewRefs(R,solt)


if __name__ == '__main__':
    main()
