import numpy as np
import matmanip as mmnip
import synth
import visu

import probdefs
import algos

import observationgenner as obsgen

def main():


    R,t = synth.FakeArucoReal() #in world coordinates
    
    visu.ViewRefs(R)

    #correct 100%
    obsR,obst = synth.SampleGenerator(R,t,noise=1,samples=1000)

    obsgen.ObsViewer(obsR,pause=False,show=False)
    
    #visu.ViewRefs([obsR[0]['R']])

    if len(R)==2:
        
        B = probdefs.rotationProbDefN2(obsR,len(R))  #95% confidence that it is correct

        B=B/len(obsR)

        print(B)

        visu.ViewRefs([np.eye(3),B])

  

    else:

        B = probdefs.rotationProbDef(obsR,len(R))  #95% confidence that it is correct

        C = np.dot(B.T,B) #C = B'B

        print("global1")
        
        rotSols = algos.RProbSolv1(C,3,len(R))
        visu.ViewRefs(rotSols)

        #converts to world coordinates or into them
        rotSolsNotUsed = mmnip.Transposer(rotSols)
        visu.ViewRefs(rotSolsNotUsed)

        #converts in first ref coordinates , 
        #rr = mmnip.genRotRelRight(rotSols)
        #visu.ViewRefs(rr)


        #converts in first ref coordinates , 
        rr = mmnip.genRotRelLeft(rotSols)
        visu.ViewRefs(rr)
    
    


if __name__ == '__main__':
    main()
