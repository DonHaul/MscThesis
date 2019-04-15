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

    R.append(Rtmat.genRotMat([213,126,32915]))
    R.append(Rtmat.genRotMat([-6,-93,7654]))

    rotRel1 =  (np.dot(R[1],R[0].T)) 

    print("original")
    print(rotRel1)

    t.append(np.array([0,0,0]))
    t.append(np.array([20,0,0]))

    t.append(np.array([0,-10,0]))
    t.append(np.array([20,-10,0]))

    #local transformation
    R.append(np.dot(R[0],Rtmat.genRotMat([0,0,-90])))
    R.append(np.dot(R[1],Rtmat.genRotMat([0,0,-90])))

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
