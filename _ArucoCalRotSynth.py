import numpy as np
import matmanip as mmnip
import synth
import visu

import probdefs
import algos

import observationgenner as obsgen

import FileIO



def main():


    R,t = synth.TestScene51() #in world coordinates

    Raux = mmnip.genRotRelLeft(R)

    #visu.ViewRefs(R,t,showRef=True,zaWordu=True)
    visu.ViewRefs(Raux)


    #correct 100%
    obsR,obst = synth.SampleGenerator(R,t,noise=0.0,samples=30)

    print(len(obsR))
    obsgen.ObsViewer(obsR,pause=False,show=False)

    if len(R)==2:
        
        B = probdefs.rotationProbDefN2(obsR,len(R))  #95% confidence that it is correct

        B=B/len(obsR)

        print(B)

        visu.ViewRefs([np.eye(3),B])

  

    else:

        B = probdefs.rotationProbDef(obsR,len(R))  #95% confidence that it is correct

        C = np.dot(B.T,B) #C = B'B

        #print("global1")
        
        #u,s,vh = np.linalg.svd(C)
        #print("WOWWOWOW")
        #print(u.shape)
        #print(vh.shape)
        


        rotSols = algos.RProbSolv1(C,3,len(R))
        #visu.ViewRefs(rotSols)

        #converts to world coordinates or into them
        rotSolsNotUsed = mmnip.Transposer(rotSols)
        
        #converts in first ref coordinates , 
        rr = mmnip.genRotRelLeft(rotSolsNotUsed)

        qrr=[]
        for r in rr:
            print(np.linalg.det(r))
            qrr.append(r.tolist())

        visu.ViewRefs(rr)


        #converts in first ref coordinates , 
        #rr = mmnip.genRotRelLeft(rotSols)
        #visu.ViewRefs(rr)

        print(rr)
        FileIO.putFileWithJson({'R':qrr},'R')


if __name__ == '__main__':
    main()
