import numpy as np
import matmanip as mmnip
import synth
import visu

import probdefs
import algos

import observationgenner as obsgen

def main():


    R,t = synth.Scenev3() #in world coordinates
    
    visu.ViewRefs(R)

    #correct 100%
    obsR,obst = synth.SampleGenerator(R,t,noise=1,samples=1000)

    #obsgen.ObsViewer(obsR,pause=True,show=False)
    
    #visu.ViewRefs([obsR[0]['R']])

    B = probdefs.rotationProbDef(obsR,len(R))  #95% confidence that it is correct


    C = np.dot(B.T,B) #C = B'B


    print("global1")
    
    rotSols = algos.RProbSolv1(C,3,len(R))
    visu.ViewRefs(rotSols)

    #converts to world coordinates or into them
    #rotSols = mmnip.Transposer(rotSols)
    #visu.ViewRefs(rotSols)

    #converts in first ref coordinates , 
    #rr = mmnip.genRotRelRight(rotSols)
    #visu.ViewRefs(rr)


    #converts in first ref coordinates , 
    rr = mmnip.genRotRelLeft(rotSols)
    visu.ViewRefs(rr)
    
    


if __name__ == '__main__':
    main()
