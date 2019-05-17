import numpy as np
import matmanip
import synth
import probdefs
import algos
import visu

import pickler as pickle

import observationgenner as obsGen

import FileIO

def main():

    R,t = synth.TiltedCams() #in world coordinates

    R = matmanip.genRotRelLeft(R)

    visu.ViewRefs(R,t)
    print(t)

    R = FileIO.getJsonFromFile("./tmp/R dugong 16-05-2019 23:28:35.json")['R']

    R = np.asarray(R)

    R = np.split(R,3,axis=0)
    
    RR = []

    for r in R:
        RR.append(np.squeeze(r))

    print(RR)
    #pprint.pprint(t)

    R=RR
    
    #correct
    obsR,obst = synth.SampleGenerator(R,t,noise=1,samples=1000)

    #IMPORTING REAL ROTATIONS, SHOW WITH AND WITHOUT THIS
    #ola = pickle.Out("static/ArucoRot.pickle")
    #R =ola["RlocalPermutated"]

    #obsGen.ObsViewer(obst,"t")


    # TRANSLATION STUFF
    A,b = probdefs.translationProbDef(obst,R,len(t))

    #x, res, rank, s = np.linalg.lstsq(A,b,rcond=None) #(A'A)^(-1) * A'b
    x= algos.LeastSquares(A,b)
    
    print("LS,LSnp,LSinv")

    x2 = np.dot(np.dot(np.linalg.pinv(np.dot(A.T,A)),A.T),b)

    print(np.sqrt(np.sum(x**2)))
    print(np.sqrt(np.sum(x2**2)))
    #print(x2)

    solsplit2 = np.split(x,len(t))
    sol=[]
    for wow in solsplit2:
        sol.append(np.squeeze(wow))

    print(sol)
    visu.ViewRefs(R,sol)

    #print(solsplit2)



    solt =[]
    #change t referential
    #for i in range(len(solsplit2)):
    #    solt.append(np.dot(-R[i].T,solsplit2[i]))


    #ViewRefs(R,solt)


if __name__ == '__main__':
    main()