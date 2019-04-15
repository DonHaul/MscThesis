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


    R,t = FakeAruco()

    ViewRefs(R,t)

    groundTruths = Rtmat.genRotRel(R)
    
    
    ViewRefs(groundTruths[0])

    #correct
    obsR,obst = SampleGenerator(R,t,noise=1)


    for i in obsR:
        
        print("From: " +str(i['from']//4+1)+" to:"+str(i['to']//4+1))
        print(i['rot'])
        ViewRefs([Rtmat.genRotMat([0,0,0]),i['rot']])


if __name__ == '__main__':
    main()
