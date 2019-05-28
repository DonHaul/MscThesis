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

    R,t = synth.TestScene51() #in world coordinates

    #R = matmanip.genRotRelLeft(R)

    visu.ViewRefs(R,t,showRef=True)
    print(t)

    R1 = FileIO.getJsonFromFile("./tmp/R chinchilla 18-05-2019 00:27:47.json")['R']

    R1 = np.asarray(R1)

    R1 = np.split(R1,4,axis=0)
    
    RR = []

    for r in R1:
        RR.append(np.squeeze(r))

    print(RR)
    #pprint.pprint(t)

    R1=RR
    
    #correct
    obsR,obst = synth.SampleGenerator(R,t,noise=1,samples=1000)


    # TRANSLATION STUFF
    A,b = probdefs.translationProbDef(obst,R1,len(t))

    #x, res, rank, s = np.linalg.lstsq(A,b,rcond=None) #(A'A)^(-1) * A'b
    x= algos.LeastSquares(A,b)
    
    #print("LS,LSnp,LSinv")
    #x2 = np.dot(np.dot(np.linalg.pinv(np.dot(A.T,A)),A.T),b)
    #print(np.sqrt(np.sum(x**2)))
    #print(np.sqrt(np.sum(x2**2)))
    #print(x2)

    solsplit2 = np.split(x,len(t))
    sol=[]
    for wow in solsplit2:
        sol.append(np.squeeze(wow))

    print(sol)
    visu.ViewRefs(R1,sol,showRef=True)

    #print(solsplit2)



    solt =[]
    #change t referential
    #for i in range(len(solsplit2)):
    #    solt.append(np.dot(-R[i].T,solsplit2[i]))


    #ViewRefs(R,solt)


if __name__ == '__main__':
    main()