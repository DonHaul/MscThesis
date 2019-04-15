import open3d
import math
import numpy as np
import pickler as pickle
import pprint
import random
import Rtmat
import phase2_sparkle as phase2
from synth import *
from decimal import Decimal

def main():

    np.set_printoptions(threshold=np.inf)
    np.set_printoptions(precision=1)

    R,t = FakeAruco()

    ViewRefs(R)

    groundTruths = Rtmat.genRotRel(R) #95% confidence that it is correct
    
    ViewRefs(groundTruths)


    #correct
    obsR,obst = SampleGenerator(R,t,noise=0.1)

    '''
    for i in obsR:
        print("From: " +str(i['from']//3+1)+" to:"+str(i['to']//3+1))
        print(i)
        ViewRefs([Rtmat.genRotMat([0,0,0]),i['rot']])
    '''

    B = phase2.problemDef(obsR,len(R))  #95% confidence that it is correct

    C = np.dot(B.T,B) #C = B'B


    rotSols = phase2.TotalLeastSquares(C,3,len(R)) #<- HAS TO BE WRONG
    
    print("global")

    ViewRefs(rotSols)

    print("local")

    #rotSoles = Rtmat.genRotRel(rotSols)
    
    rotSoles = [] #correct way to make 2d list

    #generate R between each things
    for j in range(0,len(rotSols)):
        rotSoles.append(np.dot(rotSols[0].T,rotSols[j])) #Rw2*R1w' = R12  #ASSIM FUNCIONA MAS NAO WRONG SER ASSIm isto supostamente e de todos para 1 e nao de 1 para todos


    #print("local")
    ViewRefs(rotSoles)

    #comparing with ground truth
    

if __name__ == '__main__':
    main()
