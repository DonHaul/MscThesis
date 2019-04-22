import numpy as np
import matmanip
import synth
import probdefs
import algos
import visu
import gc

def main():

    np.set_printoptions(threshold=np.inf)
    np.set_printoptions(precision=1)

    R=[]
    t=[]


    R,t = synth.FakeAruco()

    #pprint.pprint(t)

    visu.ViewRefs(R,t)
    
    obsR,obst = synth.SampleGenerator(R,t,noise=0.1,noiset=0,samples=100)
    #correct

    '''
    for i in obst:
        #print("From: " +str(i['from']//3+1)+" to:"+str(i['to']//3+1))
        print(i)
        #raw_input()
        #ViewRefs([matmanip.genRotMat([0,0,0]),i['trans']])
    '''

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

    solsplit3 = np.split(x2,len(t))
    visu.ViewRefs(R,solsplit2,refSize=0.1)

    solt =[]
    #change t referential
    #for i in range(len(solsplit2)):
    #    solt.append(np.dot(-R[i].T,solsplit2[i]))


    #ViewRefs(R,solt)


if __name__ == '__main__':
    main()