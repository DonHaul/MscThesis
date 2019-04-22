import numpy as np
import matmanip as mmnip
import synth
import visu

import probdefs
import algos

def main():

    np.set_printoptions(threshold=np.inf)
    np.set_printoptions(precision=1)

    R,t = synth.FakeArucoRotated()

    groundTruths = mmnip.genRotRel(R)

    visu.ViewRefs(R,t)


    #correct 100%
    obsR,obst = synth.SampleGenerator(R,t,noise=0.1)



    B = probdefs.rotationProbDef(obsR,len(R))  #95% confidence that it is correct

    C = np.dot(B.T,B) #C = B'B


    rotSols = algos.TotalLeastSquares(C,3,len(R)) 

    print("global")

    visu.ViewRefs(rotSols)

    print("local")
    
    rotSoles = mmnip.genRotRel(rotSols)
    
  

    #print("local")
    visu.ViewRefs(rotSoles)

    mmnip.CompareMatLists(groundTruths,rotSoles)

    

if __name__ == '__main__':
    main()
