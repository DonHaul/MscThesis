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

    print("HELP I HAVE THE BIG ")
    haha =(np.dot(B,np.vstack(rotSols)))
    ga = algos.MeanSquaredError(haha)
    print("MSE real sol",ga)

    print("")

    print("local")    
    rotSoles = mmnip.genRotRel(rotSols)    

    print("HELP I HAVE THE BIG  LOCAL")
    haha =(np.dot(B,np.vstack(rotSoles)))
    ga = algos.MeanSquaredError(haha)
    print("MSE real sol",ga)
    
    #mmnip.CompareMatLists(groundTruths,rotSoles)

    permuter = [[1,0,0],[0,0,-1],[0,1,0]]

    finalR=  mmnip.PermuteCols(rotSoles,permuter)

    print("HELP I HAVE THE BIG  LOCAL PERMUTED")
    haha =(np.dot(B,np.vstack(finalR)))
    ga = algos.MeanSquaredError(haha)
    print("MSE real sol",ga)

    
    #visu.ViewRefs( mmnip.genRotRel(finalR) )


if __name__ == '__main__':
    main()
