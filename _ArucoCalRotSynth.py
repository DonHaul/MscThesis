import numpy as np
import matmanip as mmnip
import synth
import visu

import probdefs
import algos

def main():


    R,t = synth.FakeAruco()

    groundTruths = mmnip.genRotRel(R)

    #visu.ViewRefs(R,t)
    print("ground truth")
    visu.ViewRefs(groundTruths)


    #correct 100%
    obsR,obst = synth.SampleGenerator(R,t,noise=1)



    B = probdefs.rotationProbDef(obsR,len(R))  #95% confidence that it is correct


    C = np.dot(B.T,B) #C = B'B


    rotSols = algos.TotalLeastSquares(C,3,len(R)) 

    print("global")
    visu.ViewRefs(rotSols)

     
    rotSoles = mmnip.genRotRel(rotSols)    

    print("local")   
    visu.ViewRefs(rotSoles)

    
    permuter = [[0,0,1],[-1,0,0],[0,-1,0]]

    finalR=  mmnip.PermuteCols(rotSoles,permuter)  

    print("finalR")
    visu.ViewRefs(finalR)


    
    Rrelations = []
    #generate R between each things
    for j in range(0,len(finalR)):
        Rrelations.append(np.dot(finalR[0].T,finalR[j])) #Rw2*R1w' = R12

    print("Rotated")
    visu.ViewRefs(Rrelations)


if __name__ == '__main__':
    main()
