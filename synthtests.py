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


    R=[]
    t=[]


    R,t = FakeAruco()


    ViewRefs(R,t)
    
    obsR,obst = SampleGenerator(R,t,noise=0.1)

    '''
    for i in obst:
        print("From: " +str(i['from']//3+1)+" to:"+str(i['to']//3+1))
        print(i)

        ViewRefs([Rtmat.genRotMat([0,0,0]),i['trans']])
    '''

        # TRANSLATION STUFF
    A,b = problemDef2(obst,R,len(t))

    x, res, rank, s = np.linalg.lstsq(A,b,rcond=None) #(A'A)^(-1) * A'b
    print(x,res,rank,s) 
    

    print("asahpe",np.dot(A.T,A).shape)

    x2= np.dot( np.linalg.pinv(np.dot(A.T,A)),np.dot(A.T,b)) #(A'A)^(-1) * A'b  #<= WHY USE PINV INSTEAD OF INV (WRONG?)
    #print(x2)

    print( "DIFFERENCE", sum(np.sqrt(np.square(x-x2))))

    
    print("x")

    #JANKY
    solsplit2 = np.split(x,len(t))
    print("len",len(solsplit2))
    solt =[]

    for i in range(len(solsplit2)):
        solt.append(np.dot(-R[i].T,solsplit2[i]))
 



    ViewRefs(R,solt,refSize=1)


if __name__ == '__main__':
    main()
