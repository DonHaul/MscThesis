import numpy as np
import matmanip
import synth
import probdefs
import algos
import visu

import pickler as pickle

def main():

    R,t = synth.FakeArucoReal()



    #pprint.pprint(t)

    visu.ViewRefs(R,t)
    
    obsR,obst = synth.SampleGenerator(R,t,noise=0.1,noiset=0,samples=100)
    #correct

    #IMPORTING REAL ROTATIONS, SHOW WITH AND WITHOUT THIS
    ola = pickle.Out("static/ArucoRot.pickle")
    R =ola["RlocalPermutated"]

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
    visu.ViewRefs(R,solsplit2)

    solt =[]
    #change t referential
    #for i in range(len(solsplit2)):
    #    solt.append(np.dot(-R[i].T,solsplit2[i]))


    #ViewRefs(R,solt)


if __name__ == '__main__':
    main()