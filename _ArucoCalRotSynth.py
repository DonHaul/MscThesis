import numpy as np
import matmanip as mmnip
import synth
import visu

import probdefs
import algos

def main():


    R,t = synth.FakeAruco2Markers()

    groundTruths = mmnip.genRotRel(R)

    #visu.ViewRefs(R,t)
    print("ground truth")
    visu.ViewRefs(groundTruths)


    #correct 100%
    obsR,obst = synth.SampleGenerator(R,t,noise=1)



    B = probdefs.rotationProbDef(obsR,len(R))  #95% confidence that it is correct


    C = np.dot(B.T,B) #C = B'B


    rotSols = algos.TotalLeastSquares(C,3,len(R)) 

    #print("global")
    #visu.ViewRefs(rotSols)
     
    rotSoles = mmnip.genRotRel(rotSols)    
    visu.ViewRefs(rotSoles)

    permuter = [[0,0,1],[-1,0,0],[0,-1,0]]

    #METHOD1
    finalR = mmnip.AxisSwapper(rotSoles,permuter)
    visu.ViewRefs(finalR)


    
    


if __name__ == '__main__':
    main()
