import numpy as np
import matmanip as mmnip
import synth
import visu

import probdefs
import algos

import observationgenner as obsgen

def main():


    #R,t = synth.Scenev3()
    R,t = synth.FakeAruco()
    #R,t = synth.FakeAruco()
    #R,t = synth.FakeArucoReal()
    R = mmnip.genRotRel(R)
    #visu.ViewRefs(R)
    #print(np.dot(R[0],R[1]).T)


    print(np.dot(R[0],R[1]).T)
    
    #visu.ViewRefs(R,t)
    #print("ground truth")
    #visu.ViewRefs(R)


    #correct 100%
    obsR,obst = synth.SampleGenerator(R,t,noise=1,samples=1000)

    #obsgen.ObsViewer(obsR,pause=True,show=False)
    
    #visu.ViewRefs([obsR[0]['R']])

    B = probdefs.rotationProbDef(obsR,len(R))  #95% confidence that it is correct


    C = np.dot(B.T,B) #C = B'B


    print("global1")
    rotSols = algos.RProbSolv1(C,3,len(R))    
    visu.ViewRefs(rotSols)

    print("global2")
    #rotSols = algos.RProbSolv1(C,3,len(R))    
    #visu.ViewRefs(rotSols)
     
    
    print("local1")
    
    rr = mmnip.genRotRel(rotSols)
    visu.ViewRefs(rr)
    
    print("localleft1")
    rr = mmnip.globalRotateRotsl(rotSols)
    visu.ViewRefs(rr)

    print("localweird mode")

    Rrelations = []

    #generate R between each things
    for j in range(0,len(rotSols)):
        Rrelations.append(np.dot(rotSols[j].T,rotSols[0])) #Rw2*R1w' = R12

    
    visu.ViewRefs(Rrelations)

    
    


if __name__ == '__main__':
    main()
