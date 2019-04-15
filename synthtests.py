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


    #print(x,res,rank,s)    

    x2= np.dot( np.linalg.inv(np.dot(A.T,A)),np.dot(A.T,b)) #(A'A)^(-1) * A'b

    #JANKY
    solsplit2 = np.split(x2,len(t))

    print(solsplit2[0].shape)


    ViewRefs(R,solsplit2,refSize=1)


if __name__ == '__main__':
    main()
