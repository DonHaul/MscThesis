import open3d
import math
import numpy as np
import pickler as pickle
import pprint
import random
import Rtmat
import phase2_sparkle as phase2
import synth



def main():
    print("helloworld")

    R=[]
    t=[]

    
    t0=np.array([0,0,0]))

    R01 =Rtmat.genRotMat([0,0,0])
    t01 = np.array([10,0,0])




    synth.ViewRefs(R,t)

    rotRel2 =  (np.dot(R[3],R[2].T)) 
    print("after local")
    print(rotRel2)


    #global transformation
    R.append(np.dot(Rtmat.genRotMat([0,0,-90]),R[0]))
    R.append(np.dot(Rtmat.genRotMat([0,0,-90]),R[1]))

    rotRel3 =  (np.dot(R[5],R[4].T)) 

    print("after global")
    print(rotRel3)
    



if __name__ == '__main__':
    main()
